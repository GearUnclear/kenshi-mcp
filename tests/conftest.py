from __future__ import annotations

import pytest

from kenshi_link.backends.base import Clock
from kenshi_link.backends.mock import MockBackend
from kenshi_link.config import Config
from kenshi_link.controller import Controller


class FakeClock(Clock):
    """Virtual time: sleeping advances it instantly."""

    def __init__(self) -> None:
        self.time = 0.0

    def now(self) -> float:
        return self.time

    def sleep(self, seconds: float) -> None:
        self.time += max(0.0, seconds)


@pytest.fixture
def config(tmp_path) -> Config:
    cfg = Config(backend="mock", data_dir=tmp_path / "home")
    cfg.validate()
    return cfg


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def backend(config, clock) -> MockBackend:
    return MockBackend(config, clock)


@pytest.fixture
def controller(config, backend, clock) -> Controller:
    return Controller(config, backend, clock)
