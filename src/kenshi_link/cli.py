"""Command line entry point: `kenshi-link <command>`."""

from __future__ import annotations

import argparse
import asyncio
import sys
import time
from pathlib import Path

from .config import config_path, load_config

_LOSSY_ERROR_HANDLERS = ("replace", "backslashreplace", "ignore", "xmlcharrefreplace", "namereplace")


def _tolerate_unencodable_output() -> None:
    """Make printing unable to fail on a character the output encoding lacks.

    A Windows console window takes any text. But when output is redirected to a file or
    a pipe, Python encodes it with the system code page (cp1252, cp932, ...) and raises
    on the first character outside it. What gets printed here includes Claude's own
    words and the status line, so that would end a play session part-way. Characters
    that cannot be written are shown as "?" instead; the transcript file keeps them.
    """
    stream = sys.stdout
    if stream is None or getattr(stream, "errors", None) in _LOSSY_ERROR_HANDLERS:
        return
    try:
        stream.reconfigure(errors="replace")
    except (AttributeError, ValueError, OSError):  # not a regular text stream; leave it alone
        pass


def _serve(_args: argparse.Namespace) -> int:
    from .server import main as serve

    serve()
    return 0


def _doctor(args: argparse.Namespace) -> int:
    from .controller import ControlError, Controller

    config = load_config()
    print(f"config file: {config_path()} ({'found' if config_path().is_file() else 'not present, using defaults'})")
    print(f"data directory: {config.data_dir}")
    try:
        controller = Controller(config)
    except Exception as exc:
        print(f"backend: FAILED to start - {exc}")
        return 1
    try:
        report = controller.describe()
        print(report)
        if "window: NOT FOUND" in report or "window: UNUSABLE" in report:
            return 1
        if args.screenshot:
            try:
                result = controller.observe(grid=args.grid)
            except ControlError as exc:
                print(f"screenshot: FAILED - {exc}")
                return 1
            shot = result.images[-1]
            path = Path(args.screenshot).expanduser()
            path.write_bytes(shot.data)
            print(f"screenshot: saved {shot.width}x{shot.height} {shot.format} to {path}")
            print("Open it and check that it shows the game, not a black frame or another window.")
            print(result.text.splitlines()[-1])
    finally:
        controller.close()
    return 0


def _stop(_args: argparse.Namespace) -> int:
    config = load_config()
    config.data_dir.mkdir(parents=True, exist_ok=True)
    config.stop_file.write_text(
        f"stopped with `kenshi-link stop`\n{time.strftime('%Y-%m-%d %H:%M:%S')}\n", encoding="utf-8"
    )
    print(f"Input disabled ({config.stop_file} created). Run `kenshi-link resume` to allow it again.")
    return 0


def _resume(_args: argparse.Namespace) -> int:
    config = load_config()
    if config.stop_file.exists():
        config.stop_file.unlink()
        print("Input enabled again.")
    else:
        print("Input was not disabled.")
    return 0


def _play(args: argparse.Namespace) -> int:
    from .agent import AgentOptions, play

    options = AgentOptions(
        goal=args.goal,
        model=args.model,
        effort=args.effort,
        max_steps=args.max_steps,
        max_minutes=args.max_minutes,
        fallbacks=not args.no_fallbacks,
        context_editing=not args.no_context_editing,
    )
    server_env = {"KENSHI_LINK_BACKEND": "mock"} if args.mock else None
    left: list[str] = []  # what became of the game when the session ended, in a sentence

    def game_state() -> str:
        return left[-1] if left else "The game was never reached, so it is as you left it."

    try:
        outcome = asyncio.run(play(options, server_env, left.append))
    except KeyboardInterrupt:
        print(f"\nInterrupted. {game_state()}")
        return 130
    except Exception as exc:  # API rejections, missing credentials, a server that would not start
        while isinstance(exc, BaseExceptionGroup) and exc.exceptions:
            exc = exc.exceptions[0]  # the task group wrapper hides the actual cause
        print(f"kenshi-link: the session stopped on an error: {type(exc).__name__}: {exc}", file=sys.stderr)
        if "authentication method" in str(exc):
            print("No Claude API credentials were found: set ANTHROPIC_API_KEY or run `ant auth login`.",
                  file=sys.stderr)
        print(game_state(), file=sys.stderr)
        return 1
    print()
    print(f"Session finished: {outcome.reason} after {outcome.steps} game actions.")
    if outcome.report:
        print(outcome.report)
    print(game_state())
    print(outcome.usage.summary())
    if options.transcript:
        print(f"Transcript: {options.transcript}")
    return 0 if outcome.reason in ("ended", "budget") else 1


def build_parser() -> argparse.ArgumentParser:
    from .agent import DEFAULT_MODEL

    parser = argparse.ArgumentParser(
        prog="kenshi-link", description="Let Claude see and play Kenshi."
    )
    commands = parser.add_subparsers(dest="command")

    serve = commands.add_parser("serve", help="run the MCP server on stdio (what Claude clients launch)")
    serve.set_defaults(run=_serve)

    doctor = commands.add_parser("doctor", help="check that the game window can be found and captured")
    doctor.add_argument("--screenshot", metavar="PATH", help="also save what Claude would see to this file")
    doctor.add_argument("--grid", action="store_true", help="draw the coordinate grid on that screenshot")
    doctor.set_defaults(run=_doctor)

    stop = commands.add_parser("stop", help="disable all game input immediately")
    stop.set_defaults(run=_stop)
    resume = commands.add_parser("resume", help="allow game input again after a stop")
    resume.set_defaults(run=_resume)

    play = commands.add_parser("play", help="let Claude play on its own through the Claude API")
    play.add_argument("--goal", required=True, help="what Claude should try to achieve this session")
    play.add_argument("--model", default=DEFAULT_MODEL, help=f"Claude model ID (default {DEFAULT_MODEL})")
    play.add_argument("--effort", default="medium", choices=["low", "medium", "high", "xhigh", "max"],
                      help="how hard Claude thinks each turn (default medium)")
    play.add_argument("--max-steps", type=int, default=300, help="stop after this many game actions")
    play.add_argument("--max-minutes", type=float, default=120.0, help="stop after this much wall-clock time")
    play.add_argument("--no-fallbacks", action="store_true",
                      help="do not retry a declined turn on a fallback model")
    play.add_argument("--no-context-editing", action="store_true",
                      help="do not ask the API to clear old screenshots from the context")
    play.add_argument("--mock", action="store_true", help="play the built-in stand-in window instead of Kenshi")
    play.set_defaults(run=_play)
    return parser


def main(argv: list[str] | None = None) -> int:
    _tolerate_unencodable_output()
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "run", None):
        parser.print_help()
        return 2
    try:
        return args.run(args)
    except ValueError as exc:  # configuration problems
        print(f"kenshi-link: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
