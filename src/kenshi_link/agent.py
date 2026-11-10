"""Autonomous play: Claude drives the kenshi-link MCP server by itself.

`kenshi-link play --goal "..."` starts the MCP server as a child process, hands its
tools to Claude through the Messages API, and keeps the loop going until Claude ends
the session, the budget runs out, or the operator stops it.

The conversation is strictly append-only. Old screenshots are dropped by the API's
server-side context editing rather than by rewriting history here, because current
Claude models tie their reasoning blocks to the exact history that produced them.
When the context grows very large the session "rolls over": Claude writes a handoff
into its notes file and a fresh conversation picks up from those notes.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .config import Config, load_config
from .controller import HALT_MARKER

DEFAULT_MODEL = "claude-opus-5-5"

AGENT_PREAMBLE = """\
You are playing the game Kenshi on your own, on the operator's computer. The operator set a \
goal and left you to it: they are not watching each step and cannot answer questions while you \
play, so make the decisions yourself and keep going until the goal is reached or the session's \
budget runs out.

Before each group of actions, say in one sentence what you are about to do and why; the \
operator reads this log afterwards.

Call end_session when the goal is achieved, or when you are blocked by something only the \
operator can fix (the game is not running, a crash dialog, a wrong window). Before you call \
it, pause the game and bring your notes up to date so the next session can pick up where this \
one stopped.
"""

END_TOOL: dict[str, Any] = {
    "name": "end_session",
    "description": (
        "End this play session. Call it when the goal is achieved, when the operator's budget "
        "message tells you to wrap up, or when you are blocked by something only the operator "
        "can fix. Pause the game and update your notes first."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "report": {
                "type": "string",
                "description": "What was accomplished, the current situation in the game, and "
                "anything the operator needs to know or do.",
            }
        },
        "required": ["report"],
    },
}

CONTINUE_TEXT = (
    "Keep playing toward the goal. If it is achieved, or you are blocked by something only the "
    "operator can fix, call end_session with a report instead."
)
WRAP_UP_TEXT = (
    "Operator message: this session's budget is used up. Pause the game, save if that is "
    "sensible, bring your notes up to date with notes_write, then call end_session."
)
ROLLOVER_TEXT = (
    "Operator message: this conversation is getting long and is about to be replaced by a fresh "
    "one that starts from your notes file alone. Pause the game, then rewrite your notes with "
    "notes_write(mode='replace') so they hold everything needed to continue (goal, plan and "
    "next step, squad and their condition, money, locations, how the interface behaves here, "
    "lessons learned). Then call end_session with report='rollover'."
)
_GRACE_STEPS = 8


@dataclass
class AgentOptions:
    goal: str
    model: str = DEFAULT_MODEL
    effort: str = "medium"
    max_tokens: int = 16000
    max_steps: int = 300
    max_minutes: float = 120.0
    fallbacks: bool = True
    context_editing: bool = True
    clear_trigger_tokens: int = 80_000
    clear_keep_tool_uses: int = 8
    clear_at_least_tokens: int = 30_000
    rollover_tokens: int = 400_000
    max_idle_turns: int = 3
    transcript: Path | None = None
    quiet: bool = False


@dataclass
class Usage:
    requests: int = 0
    input_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    output_tokens: int = 0

    def add(self, usage: Any) -> int:
        """Accumulate one response's usage; return the size of the context it was sent."""
        fresh = getattr(usage, "input_tokens", 0) or 0
        read = getattr(usage, "cache_read_input_tokens", 0) or 0
        written = getattr(usage, "cache_creation_input_tokens", 0) or 0
        self.requests += 1
        self.input_tokens += fresh
        self.cache_read_tokens += read
        self.cache_write_tokens += written
        self.output_tokens += getattr(usage, "output_tokens", 0) or 0
        return fresh + read + written

    def summary(self) -> str:
        return (
            f"{self.requests} requests; input {self.input_tokens:,} uncached + "
            f"{self.cache_read_tokens:,} cache-read + {self.cache_write_tokens:,} cache-write tokens; "
            f"output {self.output_tokens:,} tokens"
        )


@dataclass
class Outcome:
    reason: str  # ended | budget | halted | idle | refusal | error
    report: str = ""
    steps: int = 0
    segments: int = 1
    usage: Usage = field(default_factory=Usage)


def _attr(obj: Any, *names: str) -> Any:
    """Read a field that is spelled differently across mcp 1.x (camelCase) and 2.x (snake_case)."""
    for name in names:
        if hasattr(obj, name):
            return getattr(obj, name)
    return None


def tool_params(mcp_tools: list[Any]) -> list[dict[str, Any]]:
    """MCP tool definitions -> Messages API tool definitions, in a stable order."""
    params = [
        {
            "name": tool.name,
            "description": tool.description or "",
            "input_schema": _attr(tool, "input_schema", "inputSchema") or {"type": "object"},
        }
        for tool in sorted(mcp_tools, key=lambda t: t.name)
    ]
    return [*params, END_TOOL]


def echoable(content: list[Any]) -> list[Any]:
    """The assistant content to send back on the next request.

    Normally that is the content unchanged. After a mid-reply refusal fallback, blocks
    produced by the declined model before the last `fallback` marker must be dropped
    (except its text), and the marker itself must stay where it was.
    """
    last = max((i for i, block in enumerate(content) if block.type == "fallback"), default=-1)
    if last < 0:
        return list(content)
    kept = [
        block
        for block in content[:last]
        if block.type in ("text", "fallback")
    ]
    return [*kept, *content[last:]]


def runnable_tool_uses(content: list[Any]) -> list[Any]:
    """Tool calls that should actually run: those after the last fallback marker."""
    last = max((i for i, block in enumerate(content) if block.type == "fallback"), default=-1)
    return [block for block in content[last + 1 :] if block.type == "tool_use"]


class Agent:
    def __init__(self, client: Any, session: Any, options: AgentOptions, config: Config | None = None) -> None:
        self.client = client
        self.session = session
        self.options = options
        self.config = config or load_config()
        self.usage = Usage()
        self.steps = 0
        self.segments = 1
        self._started = time.monotonic()
        self._transcript = options.transcript

    # ---- output -----------------------------------------------------------------

    def _say(self, text: str) -> None:
        if self.options.quiet:
            return
        try:
            print(text, flush=True)
        except UnicodeEncodeError:
            # Output redirected to a file or pipe is encoded with the system code page on
            # Windows, which lacks most of what Claude may write (arrows, CJK, emoji).
            # The log line is not worth the session: print what the encoding can carry.
            encoding = getattr(sys.stdout, "encoding", None) or "ascii"
            print(text.encode(encoding, "replace").decode(encoding, "replace"), flush=True)

    def _record(self, kind: str, **fields: Any) -> None:
        if self._transcript is None:
            return
        try:
            self._transcript.parent.mkdir(parents=True, exist_ok=True)
            with self._transcript.open("a", encoding="utf-8") as out:
                out.write(json.dumps({"time": time.time(), "kind": kind, **fields}, default=str) + "\n")
        except OSError:
            pass

    # ---- the API request --------------------------------------------------------

    def _request(self, system: str, tools: list[dict[str, Any]], messages: list[Any]) -> dict[str, Any]:
        options = self.options
        betas: list[str] = []
        request: dict[str, Any] = {
            "model": options.model,
            "max_tokens": options.max_tokens,
            # Frozen for the whole session: the system prompt and tool list are part of
            # the prefix that both the prompt cache and Claude's reasoning blocks depend on.
            "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
            "tools": tools,
            "messages": messages,
            "thinking": {"type": "adaptive", "display": "summarized"},
            "output_config": {"effort": options.effort},
            "cache_control": {"type": "ephemeral"},
        }
        if options.context_editing:
            betas.append("context-management-2025-06-27")
            request["context_management"] = {
                "edits": [
                    {
                        "type": "clear_tool_uses_20250919",
                        "trigger": {"type": "input_tokens", "value": options.clear_trigger_tokens},
                        "keep": {"type": "tool_uses", "value": options.clear_keep_tool_uses},
                        "clear_at_least": {"type": "input_tokens", "value": options.clear_at_least_tokens},
                        "exclude_tools": ["notes_read", "manual"],
                    }
                ]
            }
        if options.fallbacks:
            # If a safety classifier declines a turn, the API retries it on the model
            # Anthropic recommends for that case instead of ending the session.
            betas.append("server-side-fallback-2026-07-01")
            request["fallbacks"] = "default"
        if betas:
            request["betas"] = betas
        return request

    async def _create(self, request: dict[str, Any]) -> Any:
        import anthropic

        delay = 5.0
        for attempt in range(6):
            try:
                return await self.client.beta.messages.create(**request)
            except anthropic.RateLimitError as exc:
                wait = float(exc.response.headers.get("retry-after", delay))
                self._say(f"  rate limited; waiting {wait:.0f}s")
            except anthropic.APIConnectionError:
                wait = delay
                self._say(f"  connection problem; retrying in {wait:.0f}s")
            except anthropic.APIStatusError as exc:
                if exc.status_code < 500:
                    raise
                wait = delay
                self._say(f"  API error {exc.status_code}; retrying in {wait:.0f}s")
            if attempt == 5:
                break
            await asyncio.sleep(wait)
            delay = min(delay * 2, 60.0)
        raise RuntimeError("The Claude API kept failing; giving up.")

    # ---- tools ------------------------------------------------------------------

    async def _run_tool(self, name: str, arguments: dict[str, Any]) -> tuple[list[Any] | str, bool]:
        from anthropic.lib.tools.mcp import mcp_content

        _let_the_server_take_focus()
        try:
            result = await self.session.call_tool(name, arguments)
        except Exception as exc:  # transport failure, not a tool error
            return f"The tool call failed before reaching the game: {exc}", True
        blocks = [mcp_content(item) for item in result.content]
        return blocks or "(no output)", bool(_attr(result, "is_error", "isError"))

    @staticmethod
    def _text_of(content: list[Any] | str) -> str:
        if isinstance(content, str):
            return content
        return "\n".join(block["text"] for block in content if block.get("type") == "text")

    def _over_budget(self) -> bool:
        elapsed_minutes = (time.monotonic() - self._started) / 60
        return self.steps >= self.options.max_steps or elapsed_minutes >= self.options.max_minutes

    def _opening(self, continuation: bool) -> str:
        lines = [f"Goal for this session: {self.options.goal}"]
        if continuation:
            lines.append(
                "This continues an earlier conversation that was closed to keep the context small. "
                "Everything you know is in your notes file: read it first."
            )
        lines.append("Start by reading your notes and the controls manual, then look at the game.")
        return "\n\n".join(lines)

    # ---- the loop ---------------------------------------------------------------

    async def run(self) -> Outcome:
        init = await self.session.initialize()
        system = AGENT_PREAMBLE + "\n" + (init.instructions or "")
        tools = tool_params((await self.session.list_tools()).tools)
        self._record("start", goal=self.options.goal, model=self.options.model, tools=[t["name"] for t in tools])

        messages: list[Any] = [{"role": "user", "content": self._opening(False)}]
        idle_turns = 0
        wrap_up_at: int | None = None  # step count when the wrap-up message was sent
        rollover_at: int | None = None

        def outcome(reason: str, report: str = "") -> Outcome:
            self._record("end", reason=reason, report=report, steps=self.steps, usage=self.usage.summary())
            return Outcome(reason, report, self.steps, self.segments, self.usage)

        while True:
            response = await self._create(self._request(system, tools, messages))
            context_size = self.usage.add(response.usage)
            for block in response.content:
                if block.type == "thinking" and getattr(block, "thinking", ""):
                    self._say(f"  (thinking) {block.thinking.strip()}")
                elif block.type == "text" and block.text.strip():
                    self._say(f"Claude: {block.text.strip()}")
                elif block.type == "fallback":
                    self._say(f"  [{block.from_.model} declined this turn; {block.to.model} continued]")
            self._record(
                "assistant",
                stop_reason=response.stop_reason,
                text=[b.text for b in response.content if b.type == "text"],
                tool_calls=[{"name": b.name, "input": b.input} for b in response.content if b.type == "tool_use"],
                context_tokens=context_size,
            )

            if response.stop_reason == "refusal":
                details = getattr(response, "stop_details", None)
                category = getattr(details, "category", None) if details else None
                return outcome("refusal", f"The model declined to continue (category: {category}).")

            messages.append({"role": "assistant", "content": echoable(response.content)})
            calls = runnable_tool_uses(response.content)

            if response.stop_reason == "pause_turn":
                continue
            if not calls:
                idle_turns += 1
                if idle_turns >= self.options.max_idle_turns:
                    return outcome("idle", "Claude stopped acting without ending the session.")
                reminder = WRAP_UP_TEXT if wrap_up_at is not None else CONTINUE_TEXT
                if response.stop_reason == "max_tokens":
                    reminder = "Your last reply was cut off by the output limit. " + reminder
                messages.append({"role": "user", "content": reminder})
                continue
            idle_turns = 0

            results: list[dict[str, Any]] = []
            ended: str | None = None
            halted: str | None = None
            truncated = response.stop_reason == "max_tokens"
            for call in calls:
                if truncated:
                    # The reply hit the output limit, so this call's arguments may be incomplete.
                    content: list[Any] | str = "Not run: your reply was cut off by the output limit. Send the call again."
                    is_error = True
                elif halted is not None:
                    content, is_error = "Not run: the operator stopped the session.", True
                elif call.name == "end_session":
                    ended = str((call.input or {}).get("report", "")).strip() or "(no report)"
                    content, is_error = "Session ended.", False
                else:
                    self.steps += 1
                    self._say(f"[{self.steps}] {call.name} {json.dumps(call.input, sort_keys=True)}")
                    content, is_error = await self._run_tool(call.name, dict(call.input or {}))
                    text = self._text_of(content)
                    self._say("     " + (text.splitlines()[0] if text else "(image)"))
                    self._record("tool", name=call.name, input=call.input, is_error=is_error, text=text)
                    if HALT_MARKER in text:
                        halted = text
                results.append(
                    {"type": "tool_result", "tool_use_id": call.id, "content": content, "is_error": is_error}
                )

            if halted is not None:
                return outcome("halted", halted)

            if ended is not None:
                if rollover_at is None:
                    return outcome("ended", ended)
                # Rollover: nothing from the old conversation is replayed, so no reasoning
                # block is ever sent with a history it was not produced in.
                self.segments += 1
                self._say(f"--- context rollover: starting conversation {self.segments} from the notes ---")
                self._record("rollover", segment=self.segments)
                messages = [{"role": "user", "content": self._opening(True)}]
                rollover_at = None
                continue

            # Operator messages ride along after the tool results and are never removed.
            if wrap_up_at is None and self._over_budget():
                wrap_up_at = self.steps
                results.append({"type": "text", "text": WRAP_UP_TEXT})
                self._say("--- budget reached: asking Claude to wrap up ---")
            elif wrap_up_at is None and rollover_at is None and context_size >= self.options.rollover_tokens:
                rollover_at = self.steps
                results.append({"type": "text", "text": ROLLOVER_TEXT})
                self._say("--- context is large: asking Claude to hand off to its notes ---")
            messages.append({"role": "user", "content": results})

            if wrap_up_at is not None and self.steps - wrap_up_at > _GRACE_STEPS:
                return outcome("budget", "The budget ran out and Claude did not end the session in time.")
            if rollover_at is not None and self.steps - rollover_at > _GRACE_STEPS:
                self.segments += 1
                self._say(f"--- forcing context rollover: starting conversation {self.segments} ---")
                self._record("rollover", segment=self.segments, forced=True)
                messages = [{"role": "user", "content": self._opening(True)}]
                rollover_at = None


def _let_the_server_take_focus() -> None:
    """Pass this process's right to change the front window on to the server.

    Windows only lets the program the user last worked in bring a window forward. That
    is this process (started from the console the user typed into), not the server, which
    the MCP SDK starts detached from any console. Where this process has no such right
    the call does nothing, and where the game is already in front none is needed.
    """
    if sys.platform != "win32":
        return
    try:
        import ctypes

        ctypes.windll.user32.AllowSetForegroundWindow(0xFFFFFFFF)  # ASFW_ANY
    except Exception:
        pass


def _bring_game_forward(config: Config) -> None:
    """Put Kenshi in front from this process, before the server exists (see above)."""
    if sys.platform != "win32" or not config.auto_focus or config.backend not in ("auto", "windows"):
        return
    try:
        from .backends import create_backend

        backend = create_backend(config)
        try:
            if not backend.locate().focused:
                backend.focus()
        finally:
            backend.close()
    except Exception:
        pass  # the server meets the same problem and reports it in words Claude can use


async def _pause_at_the_end(session: Any) -> str:
    """Pause the game as the session closes, and say in a sentence how that went."""
    try:
        result = await asyncio.wait_for(session.call_tool("set_speed", {"speed": "pause"}), timeout=20)
    except Exception as exc:
        return (
            f"The game could not be reached to pause it ({type(exc).__name__}), so it may still be "
            "running: check it."
        )
    text = "\n".join(getattr(item, "text", "") for item in result.content).strip()
    if _attr(result, "is_error", "isError"):
        reason = text.splitlines()[0] if text else "no reason given"
        return f"The game was not paused and may still be running: {reason}"
    return "The game is paused."


async def play(
    options: AgentOptions,
    server_env: dict[str, str] | None = None,
    on_close: Callable[[str], None] | None = None,
) -> Outcome:
    """Start the MCP server as a child process and let Claude play until the session ends.

    `on_close` is told, in a sentence, what state the game was left in.
    """
    try:
        import anthropic
    except ImportError as exc:
        raise SystemExit(
            "The autonomous runner needs the Anthropic SDK: pip install 'kenshi-link[agent]'"
        ) from exc
    from mcp import ClientSession
    from mcp.client.stdio import StdioServerParameters, stdio_client

    environment = {**os.environ, **(server_env or {})}
    config = load_config(env=environment)
    if options.transcript is None:
        options.transcript = config.sessions_dir / f"agent-{time.strftime('%Y%m%d-%H%M%S')}.jsonl"
    client = anthropic.AsyncAnthropic(max_retries=4)
    parameters = StdioServerParameters(
        command=sys.executable, args=["-m", "kenshi_link.server"], env=environment
    )
    _bring_game_forward(config)
    # errlog is named so that it is today's sys.stderr, not the one the SDK saw when imported.
    async with stdio_client(parameters, errlog=sys.stderr) as (read, write):
        async with ClientSession(read, write) as session:
            agent = Agent(client, session, options, config)
            try:
                return await agent.run()
            finally:
                # Whatever happened, do not leave the game running unattended. An advance
                # still in progress in the server is cut short by this call.
                state = "The session was cut off before the game could be paused: check whether it is running."
                try:
                    state = await _pause_at_the_end(session)
                finally:
                    if on_close is not None:
                        on_close(state)
