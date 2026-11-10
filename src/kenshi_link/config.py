"""Configuration: defaults, the keymap, and loading from a TOML file plus environment."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any

# Kenshi's default bindings. Players can rebind any of them in Options > Controls,
# so every entry can be overridden under [keymap] in the config file.
DEFAULT_KEYMAP: dict[str, str] = {
    # time
    "pause": "space",
    "speed_normal": "f2",
    "speed_fast": "f3",
    "speed_fastest": "f4",
    # camera
    "camera_forward": "w",
    "camera_back": "s",
    "camera_left": "a",
    "camera_right": "d",
    "camera_rotate_left": "q",
    "camera_rotate_right": "e",
    # windows
    "inventory": "i",
    "map": "m",
    "stats": "c",
    "research": "t",
    "crafting": "y",
    "build_mode": "b",
    # squad
    "select_all": "grave",
    "next_squad": "tab",
    "select_1": "1",
    "select_2": "2",
    "select_3": "3",
    "select_4": "4",
    "select_5": "5",
    "select_6": "6",
    "select_7": "7",
    "select_8": "8",
    "select_9": "9",
    "select_10": "0",
    # saving
    "quick_save": "f5",
    "quick_load": "f9",
    # misc
    "highlight_items": "alt",
    "close": "escape",
}

SPEEDS = ("pause", "normal", "fast", "fastest")

_DURATIONS = (
    "settle_seconds", "click_hold_seconds", "key_hold_seconds", "pointer_dwell_seconds",
    "modifier_gap_seconds", "mouse_move_seconds", "drag_seconds", "motion_probe_seconds",
    "max_advance_seconds", "max_hold_seconds",
)


def default_data_dir() -> Path:
    override = os.environ.get("KENSHI_LINK_HOME")
    return Path(override).expanduser() if override else Path.home() / ".kenshi-link"


@dataclass
class Config:
    # Which input/capture implementation to use: auto | windows | x11 | mock
    backend: str = "auto"

    # Finding the game window. On Windows the owning executable must match; on
    # Linux/Proton the X11 WM_CLASS must match. The title is a second filter.
    process_regex: str = r"(?i)^kenshi.*\.exe$"
    x11_class_regex: str = r"(?i)kenshi|steam_app_233860"
    title_regex: str = r"(?i)^kenshi"

    # Screenshots sent to Claude are scaled so the long edge is at most this.
    max_long_edge: int = 1280
    image_format: str = "jpeg"
    jpeg_quality: int = 80
    mark_pointer: bool = True  # ring the last click/drag end on the returned image

    # Timing, in seconds. Kenshi reads the mouse and the keyboard once per frame, as two
    # separate devices, so anything that must be seen in a particular order has to stay
    # put for longer than a frame. The defaults allow for about 10 frames per second.
    settle_seconds: float = 0.35  # wait after an input before the screenshot
    click_hold_seconds: float = 0.1  # how long a mouse button stays down
    key_hold_seconds: float = 0.1  # how long a key stays down
    pointer_dwell_seconds: float = 0.12  # the pointer rests on its target before a button or the wheel
    modifier_gap_seconds: float = 0.12  # between shift/ctrl/alt and the click they are held for
    mouse_move_seconds: float = 0.08
    mouse_move_steps: int = 6
    drag_seconds: float = 0.3
    motion_probe_seconds: float = 0.3
    max_advance_seconds: float = 120.0
    max_hold_seconds: float = 10.0
    halt_poll_seconds: float = 0.1  # how often a running advance or a long hold checks for a stop

    # Above this share of pixels changing between two frames, the scene is "moving".
    motion_threshold: float = 0.0001

    # Safety.
    auto_focus: bool = True  # bring Kenshi to the front when it is not focused
    allow_debug_keys: bool = False
    allow_shift_tab: bool = False  # Shift+Tab is Steam's overlay key
    failsafe_corner: bool = True  # operator parks the mouse at the screen's top-left to stop
    panic_key: bool = True  # operator holds Pause/Break to stop

    # Files.
    data_dir: Path = field(default_factory=default_data_dir)
    save_frames: bool = False  # keep every screenshot under data_dir/sessions/

    # The mock backend's window size (used for the demo and tests).
    mock_width: int = 1600
    mock_height: int = 900

    keymap: dict[str, str] = field(default_factory=lambda: dict(DEFAULT_KEYMAP))

    @property
    def stop_file(self) -> Path:
        return self.data_dir / "STOP"

    @property
    def notes_file(self) -> Path:
        return self.data_dir / "notes.md"

    @property
    def sessions_dir(self) -> Path:
        return self.data_dir / "sessions"

    def validate(self) -> None:
        from .keys import check_allowed, parse_combo

        if self.backend not in ("auto", "windows", "x11", "mock"):
            raise ValueError(f"backend must be auto, windows, x11 or mock (got {self.backend!r})")
        if self.image_format.lower() not in ("jpeg", "jpg", "png"):
            raise ValueError(f"image_format must be jpeg or png (got {self.image_format!r})")
        if not 64 <= self.max_long_edge <= 2576:
            raise ValueError("max_long_edge must be between 64 and 2576")
        for name in _DURATIONS:
            if getattr(self, name) < 0:
                raise ValueError(f"{name} cannot be negative")
        if not 0.01 <= self.halt_poll_seconds <= 1:
            raise ValueError("halt_poll_seconds must be between 0.01 and 1")
        for action, combo in self.keymap.items():
            try:
                mods, key = parse_combo(combo)
                check_allowed(
                    mods, key, allow_debug_keys=self.allow_debug_keys, allow_shift_tab=self.allow_shift_tab
                )
            except Exception as exc:
                raise ValueError(f"keymap entry {action} = {combo!r} is not usable: {exc}") from exc
        for required in ("pause", "speed_normal", "speed_fast", "speed_fastest"):
            if required not in self.keymap:
                raise ValueError(f"keymap is missing the required action {required!r}")


def config_path() -> Path:
    override = os.environ.get("KENSHI_LINK_CONFIG")
    return Path(override).expanduser() if override else default_data_dir() / "config.toml"


def _coerce(name: str, current: Any, value: Any) -> Any:
    if isinstance(current, bool):
        if isinstance(value, str):
            return value.strip().lower() in ("1", "true", "yes", "on")
        return bool(value)
    if isinstance(current, int) and not isinstance(current, bool):
        return int(value)
    if isinstance(current, float):
        return float(value)
    if isinstance(current, Path):
        return Path(str(value)).expanduser()
    if isinstance(current, str):
        return str(value)
    raise ValueError(f"cannot set {name}")


def load_config(path: Path | None = None, env: dict[str, str] | None = None) -> Config:
    """Build a Config from defaults, then the TOML file (if any), then KENSHI_LINK_* variables."""
    env = os.environ if env is None else env
    config = Config()
    path = path or config_path()
    known = {f.name for f in fields(Config)}

    if path.is_file():
        try:
            # utf-8-sig: Windows editors and PowerShell often put a byte-order mark at the
            # start of a UTF-8 file, which TOML itself does not allow.
            data = tomllib.loads(path.read_text(encoding="utf-8-sig"))
        except UnicodeDecodeError as exc:
            raise ValueError(f"{path} is not UTF-8 text; save it with UTF-8 encoding ({exc})") from exc
        except tomllib.TOMLDecodeError as exc:
            raise ValueError(f"{path}: {exc}") from exc
        for key, value in data.items():
            if key == "keymap":
                if not isinstance(value, dict):
                    raise ValueError("[keymap] must be a table of action = \"key\" pairs")
                config.keymap.update({str(k): str(v) for k, v in value.items()})
            elif key in known:
                setattr(config, key, _coerce(key, getattr(config, key), value))
            else:
                raise ValueError(f"unknown setting {key!r} in {path}")

    for item in fields(Config):
        if item.name == "keymap":
            continue
        variable = f"KENSHI_LINK_{item.name.upper()}"
        if variable in env:
            setattr(config, item.name, _coerce(item.name, getattr(config, item.name), env[variable]))
    if "KENSHI_LINK_HOME" in env and "KENSHI_LINK_DATA_DIR" not in env:
        config.data_dir = Path(env["KENSHI_LINK_HOME"]).expanduser()

    config.validate()
    return config
