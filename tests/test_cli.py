"""The command line against the stand-in window: doctor, stop and resume, output that the
console encoding cannot carry, and `play` against a scripted stand-in for the Claude API."""

from __future__ import annotations

import io
import json
import socket
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from kenshi_link import cli
from kenshi_link.controller import HALT_MARKER


@pytest.fixture
def home(tmp_path, monkeypatch):
    for variable in ("KENSHI_LINK_CONFIG", "KENSHI_LINK_DATA_DIR"):
        monkeypatch.delenv(variable, raising=False)
    monkeypatch.setenv("KENSHI_LINK_HOME", str(tmp_path / "home"))
    monkeypatch.setenv("KENSHI_LINK_BACKEND", "mock")
    monkeypatch.setenv("KENSHI_LINK_MOTION_PROBE_SECONDS", "0.02")
    return tmp_path / "home"


def redirected_stdout(monkeypatch, encoding: str) -> io.BytesIO:
    """Make sys.stdout what Python gives a program on Windows whose output goes to a file or
    a pipe: the system code page, with an error handler that raises on other characters."""
    raw = io.BytesIO()
    monkeypatch.setattr(sys, "stdout", io.TextIOWrapper(raw, encoding=encoding, errors="surrogateescape"))
    return raw


def test_doctor_reports_the_window_and_saves_a_screenshot(home, tmp_path, capsys):
    shot = tmp_path / "check.jpg"
    assert cli.main(["doctor", "--screenshot", str(shot), "--grid"]) == 0
    out = capsys.readouterr().out
    assert "backend: mock" in out and "stop file: absent" in out and str(shot) in out
    assert f"data directory: {home}" in out
    assert shot.read_bytes()[:2] == b"\xff\xd8"


def test_stop_and_resume_round_trip(home, tmp_path, capsys):
    assert cli.main(["stop"]) == 0
    assert (home / "STOP").read_text(encoding="utf-8").startswith("stopped with `kenshi-link stop`\n")
    assert cli.main(["doctor", "--screenshot", str(tmp_path / "check.jpg")]) == 1
    out = capsys.readouterr().out
    assert "stop file: PRESENT" in out and HALT_MARKER in out and not (tmp_path / "check.jpg").exists()
    assert cli.main(["resume"]) == 0 and not (home / "STOP").exists()
    assert cli.main(["resume"]) == 0
    assert capsys.readouterr().out.splitlines() == ["Input enabled again.", "Input was not disabled."]


@pytest.mark.parametrize("encoding", ["cp932", "ascii"])  # neither has the status line's middle dot
def test_output_the_console_encoding_lacks_does_not_stop_a_command(home, tmp_path, monkeypatch, encoding):
    raw = redirected_stdout(monkeypatch, encoding)
    assert cli.main(["doctor", "--screenshot", str(tmp_path / "check.jpg")]) == 0
    sys.stdout.flush()
    last = raw.getvalue().decode(encoding).splitlines()[-1]
    assert last.startswith("[game PAUSED (inferred) ? speed unknown ? screenshot 1280x720")


def test_printing_claudes_words_cannot_fail(monkeypatch):
    raw = redirected_stdout(monkeypatch, "cp1252")
    with pytest.raises(UnicodeEncodeError):
        print("mined copper \u2192 sold it \u2713")
    cli._tolerate_unencodable_output()
    print("mined copper \u2192 sold it \u2713 caf\u00e9 \u65e5\u672c \U0001f3ae")
    sys.stdout.flush()
    assert raw.getvalue().decode("cp1252").splitlines() == ["mined copper ? sold it ? caf\u00e9 ?? ?"]


# ---- play ----------------------------------------------------------------------------


@pytest.fixture
def scripted_api(monkeypatch):
    """A local HTTP server that answers the Messages API with replies given in advance.
    `kenshi-link play` is pointed at it; no request leaves this machine."""
    names = ("TCP_KEEPINTVL", "TCP_KEEPCNT", "TCP_KEEPIDLE")
    keep_alive = [getattr(socket, name) for name in names if hasattr(socket, name)]
    with socket.socket() as probe:
        try:
            for option in keep_alive:
                probe.setsockopt(socket.IPPROTO_TCP, option, 60)
        except OSError as exc:
            # The Anthropic SDK sets these on every connection. Windows has had them since
            # 2017; Wine 9.0 has not, and there every request fails and is retried for minutes.
            pytest.skip(f"this system rejects TCP keep-alive options the Anthropic SDK needs ({exc})")
    replies: list[list[dict]] = []
    requests: list[dict] = []

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args) -> None:
            pass

        def do_POST(self) -> None:
            requests.append(json.loads(self.rfile.read(int(self.headers["content-length"]))))
            content = replies.pop(0) if replies else [call(99, "end_session", report="script exhausted")]
            calls_a_tool = any(block["type"] == "tool_use" for block in content)
            body = json.dumps({
                "id": f"msg_{len(requests)}", "type": "message", "role": "assistant", "model": "claude-opus-5-5",
                "stop_sequence": None, "stop_reason": "tool_use" if calls_a_tool else "end_turn", "content": content,
                "usage": {"input_tokens": 1000, "output_tokens": 50, "cache_read_input_tokens": 0,
                          "cache_creation_input_tokens": 0},
            }).encode("utf-8")
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    for variable in ("HTTPS_PROXY", "HTTP_PROXY", "ALL_PROXY", "https_proxy", "http_proxy", "all_proxy",
                     "ANTHROPIC_AUTH_TOKEN"):
        monkeypatch.delenv(variable, raising=False)
    monkeypatch.setenv("NO_PROXY", "*")
    monkeypatch.setenv("ANTHROPIC_BASE_URL", f"http://127.0.0.1:{server.server_address[1]}")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("KENSHI_LINK_SETTLE_SECONDS", "0.02")
    try:
        yield replies, requests
    finally:
        server.shutdown()
        server.server_close()


def call(index: int, name: str, **arguments) -> dict:
    return {"type": "tool_use", "id": f"toolu_{index}", "name": name, "input": arguments}


def test_play_runs_a_session_and_says_how_the_game_was_left(home, scripted_api, capfd):
    pytest.importorskip("anthropic")
    replies, requests = scripted_api
    replies += [
        [{"type": "text", "text": "Looking first."}, call(1, "observe")],
        [call(2, "set_speed", speed="normal")],  # ... and ends the session with the clock running
        [call(3, "end_session", report="Left it running.")],
    ]
    assert cli.main(["play", "--mock", "--goal", "Watch.", "--max-steps", "5"]) == 0
    out = capfd.readouterr().out.replace("\r\n", "\n")
    assert "Claude: Looking first." in out and "[2] set_speed" in out
    assert "Session finished: ended after 2 game actions.\nLeft it running.\nThe game is paused.\n" in out
    assert len(requests) == 3 and requests[0]["model"] == "claude-opus-5-5"
    actions = [json.loads(line)["action"] for path in (home / "sessions").glob("2*.jsonl")
               for line in path.read_text(encoding="utf-8").splitlines()]
    assert actions == ["observe", "set_speed", "set_speed"], "the runner paused the game on the way out"


def test_play_does_not_claim_a_pause_it_could_not_make(home, scripted_api, capfd):
    pytest.importorskip("anthropic")
    replies, _ = scripted_api
    replies += [[call(1, "click", x=10, y=10)]]
    home.mkdir(parents=True)
    (home / "STOP").write_text("operator stop\n", encoding="utf-8")
    assert cli.main(["play", "--mock", "--goal", "Click.", "--max-steps", "5"]) == 1
    out, err = capfd.readouterr()
    assert "Session finished: halted after 1 game actions." in out, err
    assert "The game was not paused and may still be running: " in out
    assert f"{HALT_MARKER}: operator stop." in out.split("may still be running: ")[1].splitlines()[0]
    assert "The game is paused." not in out
