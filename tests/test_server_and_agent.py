"""End to end: the real MCP server as a child process (stand-in window), a real MCP client,
and the autonomous loop talking to a scripted stand-in for the Claude API."""

from __future__ import annotations

import asyncio
import io
import json
import os
import subprocess
import sys
import time
from contextlib import asynccontextmanager
from types import SimpleNamespace

import pytest
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from kenshi_link.agent import (
    CONTINUE_TEXT,
    ROLLOVER_TEXT,
    WRAP_UP_TEXT,
    Agent,
    AgentOptions,
    echoable,
    runnable_tool_uses,
)
from kenshi_link.config import Config
from kenshi_link.controller import HALT_MARKER

anthropic = pytest.importorskip("anthropic")
import httpx2  # noqa: E402  (the HTTP library the Anthropic SDK is built on)


@asynccontextmanager
async def mcp_session(home):
    env = {**os.environ, "KENSHI_LINK_BACKEND": "mock", "KENSHI_LINK_HOME": str(home),
           "KENSHI_LINK_SETTLE_SECONDS": "0.02", "KENSHI_LINK_MOTION_PROBE_SECONDS": "0.05"}
    parameters = StdioServerParameters(command=sys.executable, args=["-m", "kenshi_link.server"], env=env)
    async with stdio_client(parameters) as (read, write):
        async with ClientSession(read, write) as session:
            yield session


def is_error(result) -> bool:
    return bool(getattr(result, "is_error", getattr(result, "isError", False)))


# ---- the MCP server ------------------------------------------------------------


async def test_server_lists_tools_and_returns_screenshots(tmp_path):
    async with mcp_session(tmp_path) as session:
        init = await session.initialize()
        assert "advance(seconds, speed)" in init.instructions
        tools = {tool.name for tool in (await session.list_tools()).tools}
        assert tools == {
            "observe", "zoom", "click", "drag", "scroll", "press_key", "type_text", "hotkey",
            "camera", "advance", "set_speed", "sync_pause", "notes_read", "notes_write",
            "lookup", "lookup_topics", "manual",
        }
        assert "lookup(query)" in init.instructions and "lookup_topics" in init.instructions

        observed = await session.call_tool("observe", {})
        assert [c.type for c in observed.content] == ["text", "image"] and not is_error(observed)
        assert observed.content[1].mime_type == "image/jpeg" if hasattr(observed.content[1], "mime_type") \
            else observed.content[1].mimeType == "image/jpeg"

        advanced = await session.call_tool("advance", {"seconds": 0.3, "speed": "fast", "frames": 1})
        assert [c.type for c in advanced.content] == ["text", "image", "image"]
        assert "then paused it" in advanced.content[0].text


async def test_server_reports_errors_in_words_claude_can_use(tmp_path):
    async with mcp_session(tmp_path) as session:
        await session.initialize()
        outside = await session.call_tool("click", {"x": 99999, "y": 5})
        assert is_error(outside) and "outside the 1280x720 screenshot" in outside.content[0].text
        blocked = await session.call_tool("press_key", {"key": "alt+tab"})
        assert is_error(blocked) and "blocked" in blocked.content[0].text
        unknown = await session.call_tool("manual", {"topic": "cheats"})
        assert is_error(unknown) and "controls" in unknown.content[0].text


async def test_notes_persist_and_manual_reads(tmp_path):
    async with mcp_session(tmp_path) as session:
        await session.initialize()
        assert "empty" in (await session.call_tool("notes_read", {})).content[0].text
        await session.call_tool("notes_write", {"text": "# Goal\nReach the Hub"})
        assert "Reach the Hub" in (await session.call_tool("notes_read", {})).content[0].text
        assert "KENSHI CONTROLS" in (await session.call_tool("manual", {"topic": "controls"})).content[0].text
    assert "Reach the Hub" in (tmp_path / "notes.md").read_text()


# ---- the reference ---------------------------------------------------------------------


async def test_the_reference_is_searched_and_indexed_through_the_server(tmp_path):
    async with mcp_session(tmp_path) as session:
        await session.initialize()
        tools = {tool.name: tool for tool in (await session.list_tools()).tools}
        assert "lookup_topics" in tools["lookup"].description, "a search that finds nothing points at the index"

        found = await session.call_tool("lookup", {"query": "stop bleeding"})
        text = found.content[0].text
        assert not is_error(found) and [c.type for c in found.content] == ["text"]
        assert text.startswith("## ") and "bandage" in text.lower() and len(text) <= 6000

        one = await session.call_tool("lookup", {"query": "The Hub", "limit": 1})
        assert one.content[0].text.count("\n## ") == 0 and one.content[0].text.startswith("## ")

        missed = await session.call_tool("lookup", {"query": "Skuin"})
        assert not is_error(missed) and "Closest headings:" in missed.content[0].text
        assert "Squin" in missed.content[0].text
        empty = await session.call_tool("lookup", {"query": "?!"})
        assert not is_error(empty) and "Nothing to look up" in empty.content[0].text

        index = await session.call_tool("lookup_topics", {})
        assert index.content[0].text.startswith("Kenshi reference: ") and "16 files" in index.content[0].text
        assert len(index.content[0].text) <= 12000
        combat = await session.call_tool("lookup_topics", {"file": "combat"})
        assert 'in 1 file matching "combat"' in combat.content[0].text
        assert "and " not in combat.content[0].text.splitlines()[-1][-12:], "one file is listed in full"
        nowhere = await session.call_tool("lookup_topics", {"file": "spaceships"})
        assert not is_error(nowhere) and "The files are:" in nowhere.content[0].text

        bad = await session.call_tool("lookup", {"query": "the hub", "limit": 0})
        assert is_error(bad)
    assert not (tmp_path / "sessions").exists(), "looking something up does not touch the game"


async def test_stop_file_halts_the_server(tmp_path):
    async with mcp_session(tmp_path) as session:
        await session.initialize()
        (tmp_path / "STOP").write_text("operator stop\n")
        halted = await session.call_tool("click", {"x": 10, "y": 10})
        assert is_error(halted) and HALT_MARKER in halted.content[0].text


async def test_a_pause_does_not_wait_behind_a_long_advance(tmp_path):
    async with mcp_session(tmp_path) as session:
        await session.initialize()
        await session.call_tool("observe", {})

        async def pause_soon():
            await asyncio.sleep(1.0)
            return await session.call_tool("set_speed", {"speed": "pause"})

        started = time.monotonic()
        advanced, paused = await asyncio.gather(
            session.call_tool("advance", {"seconds": 60, "speed": "fast", "frames": 0}), pause_soon()
        )
        assert time.monotonic() - started < 15, "the pause was not queued behind the whole run"
        assert not is_error(advanced) and not is_error(paused)
        assert "less than the 60s asked for, because a pause was asked for" in advanced.content[0].text
        assert "already paused" in paused.content[0].text
        # Nothing lingers: the next run takes its full time.
        again = await session.call_tool("advance", {"seconds": 0.5, "speed": "normal", "frames": 0})
        assert "Ran the game for 0.5s" in again.content[0].text and "less than" not in again.content[0].text


def test_the_server_pauses_the_game_and_exits_when_its_client_goes_away(tmp_path):
    """A client that closes or crashes just closes the server's stdin. MCP clients then
    allow about two seconds before killing the server, and whatever it holds down stays down."""
    env = {**os.environ, "KENSHI_LINK_BACKEND": "mock", "KENSHI_LINK_HOME": str(tmp_path),
           "KENSHI_LINK_SETTLE_SECONDS": "0.02", "KENSHI_LINK_MOTION_PROBE_SECONDS": "0.05"}
    server = subprocess.Popen([sys.executable, "-m", "kenshi_link.server"], env=env, stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    def send(message: dict) -> None:
        server.stdin.write((json.dumps(message) + "\n").encode())
        server.stdin.flush()

    try:
        send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "0"}}})
        assert b'"result"' in server.stdout.readline()
        send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
              "params": {"name": "advance", "arguments": {"seconds": 60, "speed": "fast", "frames": 0}}})
        time.sleep(2.5)  # the run is under way, the game unpaused
        closed = time.monotonic()
        server.stdin.close()
        server.wait(timeout=10)
        took = time.monotonic() - closed
    finally:
        if server.poll() is None:
            server.kill()
            server.wait()
    assert took < 2.0, f"the server took {took:.1f}s to exit; a client would have killed it mid-run"
    records = [json.loads(line) for path in (tmp_path / "sessions").glob("*.jsonl")
               for line in path.read_text(encoding="utf-8").splitlines()]
    assert [record["action"] for record in records] == ["advance"]
    assert records[0]["result"].startswith("Shutting down: the run was stopped after")
    assert records[0]["result"].endswith("the game was paused.")


# ---- the autonomous loop -------------------------------------------------------


class ScriptedAPI:
    """Answers /v1/messages with pre-written replies and remembers what it was sent."""

    def __init__(self, replies: list[dict]) -> None:
        self.replies = list(replies)
        self.requests: list[dict] = []
        self.headers: list[dict] = []

    def handler(self, request: httpx2.Request) -> httpx2.Response:
        self.requests.append(json.loads(request.content))
        self.headers.append(dict(request.headers))
        reply = self.replies.pop(0)
        body = {
            "id": f"msg_{len(self.requests)}", "type": "message", "role": "assistant",
            "model": "claude-opus-5-5", "stop_sequence": None,
            "stop_reason": reply.get("stop_reason", "tool_use" if any(b["type"] == "tool_use" for b in reply["content"]) else "end_turn"),
            "content": reply["content"],
            "usage": {"input_tokens": reply.get("input_tokens", 1000), "output_tokens": 50,
                      "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
        }
        return httpx2.Response(200, json=body)

    def client(self):
        return anthropic.AsyncAnthropic(
            api_key="test-key", max_retries=0,
            http_client=anthropic.DefaultAsyncHttpxClient(transport=httpx2.MockTransport(self.handler)),
        )


def call(index: int, name: str, **arguments) -> dict:
    return {"type": "tool_use", "id": f"toolu_{index}", "name": name, "input": arguments}


def text(value: str) -> dict:
    return {"type": "text", "text": value}


def thinking(index: int) -> dict:
    return {"type": "thinking", "thinking": "Considering the next move.", "signature": f"sig{index}"}


async def run_agent(tmp_path, replies, **options):
    api = ScriptedAPI(replies)
    config = Config(backend="mock", data_dir=tmp_path)
    options = {"quiet": True, "transcript": tmp_path / "t.jsonl", **options}
    async with mcp_session(tmp_path) as session:
        agent = Agent(api.client(), session, AgentOptions(goal="Select unit 2 and move it.", **options), config)
        outcome = await agent.run()
    return api, outcome


async def test_agent_plays_a_scripted_session(tmp_path):
    api, outcome = await run_agent(tmp_path, [
        {"content": [thinking(1), text("Reading notes and looking."), call(1, "notes_read"), call(2, "observe")]},
        {"content": [thinking(2), call(3, "click", x=688, y=424)]},
        {"content": [call(4, "advance", seconds=0.3, speed="normal", frames=1)]},
        {"content": [text("That went well.")]},
        {"content": [call(5, "end_session", report="Unit 2 selected and moved.")]},
    ])
    assert outcome.reason == "ended" and outcome.report == "Unit 2 selected and moved."
    assert outcome.steps == 4 and outcome.usage.requests == 5

    first = api.requests[0]
    assert first["model"] == "claude-opus-5-5"
    assert first["thinking"] == {"type": "adaptive", "display": "summarized"}
    assert first["output_config"] == {"effort": "medium"}
    assert first["fallbacks"] == "default"
    assert first["context_management"]["edits"][0]["type"] == "clear_tool_uses_20250919"
    assert first["system"][0]["cache_control"] == {"type": "ephemeral"}
    betas = api.headers[0]["anthropic-beta"]
    assert "context-management-2025-06-27" in betas and "server-side-fallback-2026-07-01" in betas
    names = [tool["name"] for tool in first["tools"]]
    assert names[-1] == "end_session" and names[:-1] == sorted(names[:-1]) and len(names) == 18
    assert "Select unit 2" in first["messages"][0]["content"]

    # The history is append-only and the prefix (system, tools) never changes.
    for earlier, later in zip(api.requests, api.requests[1:]):
        assert later["system"] == earlier["system"] and later["tools"] == earlier["tools"]
        assert later["messages"][: len(earlier["messages"])] == earlier["messages"]

    # Both parallel tool results came back in one user message, screenshot included,
    # and the thinking block was returned untouched.
    second = api.requests[1]["messages"]
    assert second[1]["content"][0] == thinking(1)
    results = second[2]["content"]
    assert [r["tool_use_id"] for r in results] == ["toolu_1", "toolu_2"]
    kinds = [block["type"] for block in results[1]["content"]]
    assert kinds == ["text", "image"] and results[1]["content"][1]["source"]["media_type"] == "image/jpeg"

    # A turn without tool calls is answered with a nudge to continue.
    assert api.requests[4]["messages"][-1] == {"role": "user", "content": CONTINUE_TEXT}
    assert (tmp_path / "t.jsonl").read_text().count('"kind": "tool"') == 4


async def test_agent_wraps_up_when_the_budget_runs_out(tmp_path):
    api, outcome = await run_agent(tmp_path, [
        {"content": [call(1, "observe")]},
        {"content": [call(2, "notes_write", text="handoff"), call(3, "end_session", report="Budget reached.")]},
    ], max_steps=1)
    assert outcome.reason == "ended" and outcome.report == "Budget reached."
    last_user = api.requests[1]["messages"][-1]["content"]
    assert last_user[-1] == {"type": "text", "text": WRAP_UP_TEXT}
    assert last_user[0]["type"] == "tool_result"


async def test_agent_rolls_over_to_a_fresh_conversation(tmp_path):
    api, outcome = await run_agent(tmp_path, [
        {"content": [thinking(1), call(1, "observe")], "input_tokens": 500_000},
        {"content": [call(2, "notes_write", text="handoff", mode="replace"), call(3, "end_session", report="rollover")]},
        {"content": [call(4, "end_session", report="Done after rollover.")]},
    ])
    assert outcome.reason == "ended" and outcome.segments == 2
    assert api.requests[1]["messages"][-1]["content"][-1] == {"type": "text", "text": ROLLOVER_TEXT}
    fresh = api.requests[2]["messages"]
    assert len(fresh) == 1 and "read it first" in fresh[0]["content"]
    assert "thinking" not in json.dumps(fresh), "no reasoning block is replayed into the new conversation"
    assert (tmp_path / "notes.md").read_text() == "handoff\n"


async def test_agent_stops_when_the_operator_halts(tmp_path):
    (tmp_path / "STOP").write_text("operator stop\n")
    api, outcome = await run_agent(tmp_path, [
        {"content": [call(1, "click", x=10, y=10), call(2, "click", x=20, y=20)]},
    ])
    assert outcome.reason == "halted" and HALT_MARKER in outcome.report
    assert outcome.steps == 1, "the second call was not sent to the game"


async def test_agent_looks_things_up_and_is_not_stopped_by_text_that_mentions_a_stop(tmp_path):
    quoted = f"If a result contains {HALT_MARKER}, the operator has stopped the session."
    api, outcome = await run_agent(tmp_path, [
        {"content": [call(1, "lookup", query="stop bleeding"), call(2, "notes_write", text=quoted)]},
        {"content": [call(3, "notes_read")]},  # hands the marker back: a note, not a stop
        {"content": [call(4, "end_session", report="Done.")]},
    ])
    assert outcome.reason == "ended" and outcome.steps == 3
    looked_up = api.requests[1]["messages"][2]["content"][0]
    assert looked_up["is_error"] is False and looked_up["content"][0]["text"].startswith("## ")
    read_back = api.requests[2]["messages"][4]["content"][0]
    assert HALT_MARKER in read_back["content"][0]["text"] and read_back["is_error"] is False


async def test_agent_reports_a_refusal_and_gives_up_on_silence(tmp_path):
    _, refused = await run_agent(tmp_path, [{"content": [], "stop_reason": "refusal"}])
    assert refused.reason == "refusal"
    _, idle = await run_agent(tmp_path, [{"content": [text("Hm.")]}] * 3)
    assert idle.reason == "idle"


async def test_truncated_tool_calls_are_not_run(tmp_path):
    api, outcome = await run_agent(tmp_path, [
        {"content": [call(1, "click", x=10)], "stop_reason": "max_tokens"},
        {"content": [call(2, "end_session", report="ok")]},
    ])
    assert outcome.steps == 0
    result = api.requests[1]["messages"][-1]["content"][0]
    assert result["is_error"] and "cut off" in result["content"]


async def test_the_log_survives_text_the_console_cannot_encode(tmp_path, monkeypatch):
    # Output redirected to a file or pipe on Windows: the system code page, and an error
    # handler that raises on anything outside it. Claude writes arrows, CJK and emoji.
    raw = io.BytesIO()
    monkeypatch.setattr(sys, "stdout", io.TextIOWrapper(raw, encoding="cp1252", errors="surrogateescape"))
    odd = "caf\u00e9 \u2192 \u2713 \u65e5\u672c\u8a9e \U0001f3ae"
    _, outcome = await run_agent(tmp_path, [
        {"content": [{"type": "thinking", "thinking": f"Plan {odd}", "signature": "sig1"},
                     text(f"Looking {odd}"), call(1, "observe")]},
        {"content": [call(2, "manual", topic=f"no such topic {odd}")]},
        {"content": [call(3, "end_session", report=f"Done {odd}")]},
    ], quiet=False)
    sys.stdout.flush()
    printed = raw.getvalue().decode("cp1252")
    assert outcome.reason == "ended" and outcome.steps == 2 and outcome.report == f"Done {odd}"
    assert "(thinking) Plan caf\u00e9 ? ? ??? ?" in printed and "Claude: Looking caf\u00e9 ? ? ??? ?" in printed
    assert "[1] observe {}" in printed and "[2] manual" in printed
    # The transcript file keeps what the console could not show.
    records = [json.loads(line) for line in (tmp_path / "t.jsonl").read_text(encoding="utf-8").splitlines()]
    assert [f"Looking {odd}"] in [record.get("text") for record in records]


def test_fallback_turns_are_echoed_per_the_api_rules():
    def block(kind, **fields):
        return SimpleNamespace(type=kind, **fields)

    content = [
        block("thinking"), block("text", text="partial"), block("tool_use", name="click"),
        block("fallback"), block("thinking"), block("tool_use", name="observe"),
    ]
    assert [b.type for b in echoable(content)] == ["text", "fallback", "thinking", "tool_use"]
    assert [b.name for b in runnable_tool_uses(content)] == ["observe"]
    plain = [block("thinking"), block("tool_use", name="observe")]
    assert echoable(plain) == plain and len(runnable_tool_uses(plain)) == 1
