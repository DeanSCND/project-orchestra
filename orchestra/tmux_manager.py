"""libtmux-backed session management utilities for the Orchestra MVP."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Iterable, Iterator, List, Optional

import shlex

from libtmux import Server
from libtmux.exc import LibTmuxException
from libtmux.pane import Pane


class TmuxError(RuntimeError):
    """Wrapped libtmux errors for a cleaner public interface."""


@dataclass
class PaneCapture:
    """Container for captured pane output and metadata."""

    session: str
    pane: str
    lines: List[str]
    dead: bool


class TmuxManager:
    """High-level helpers around libtmux for Orchestra."""

    def __init__(
        self,
        tmux_binary: str = "tmux",
        *,
        spawn_timeout: float | None = None,
        spawn_poll_interval: float | None = None,
    ) -> None:
        try:
            self._server = Server(command=tmux_binary)
        except LibTmuxException as exc:
            raise TmuxError(str(exc)) from exc
        self._spawn_timeout = spawn_timeout or float(os.getenv("ORCHESTRA_TMUX_SPAWN_TIMEOUT", "5.0"))
        self._spawn_poll_interval = spawn_poll_interval or float(
            os.getenv("ORCHESTRA_TMUX_SPAWN_POLL_INTERVAL", "0.05")
        )

    # ------------------------------------------------------------------
    # Session lifecycle
    # ------------------------------------------------------------------
    def session_exists(self, session_name: str) -> bool:
        try:
            result = self._server.cmd("has-session", "-t", session_name)
        except LibTmuxException as exc:
            message = str(exc)
            if "no server running" in message:
                return False
            raise TmuxError(message) from exc
        return result.returncode == 0

    def spawn_session(
        self,
        session_name: str,
        command: Optional[Iterable[str]] = None,
        *,
        start_directory: Optional[str] = None,
        kill_existing: bool = False,
    ) -> None:
        if self.session_exists(session_name):
            if kill_existing:
                self.kill_session(session_name)
            else:
                raise TmuxError(f"tmux session '{session_name}' already exists")

        window_command = None
        if command:
            window_command = shlex.join(command)

        cmd: list[str] = ["new-session", "-d", "-s", session_name]
        if start_directory:
            cmd.extend(["-c", start_directory])
        if window_command:
            cmd.append(window_command)

        result = self._cmd(*cmd)
        if result.returncode != 0:
            raise TmuxError("\n".join(result.stderr))

        deadline = time.monotonic() + self._spawn_timeout
        while time.monotonic() < deadline:
            if self.session_exists(session_name):
                break
            time.sleep(self._spawn_poll_interval)
        else:
            raise TmuxError(f"tmux session '{session_name}' was not ready after {self._spawn_timeout} seconds")

    def list_sessions(self) -> List[str]:
        try:
            result = self._server.cmd("list-sessions", "-F", "#S")
        except LibTmuxException as exc:
            message = str(exc)
            if "no server running" in message:
                return []
            raise TmuxError(message) from exc

        if result.returncode != 0:
            return []
        return [line.strip() for line in result.stdout]

    def kill_session(self, session_name: str) -> None:
        session = self._find_session(session_name)
        if session is None:
            return
        try:
            session.kill_session()
        except LibTmuxException as exc:
            raise TmuxError(str(exc)) from exc

    def attach_session(self, session_name: str) -> None:
        try:
            self._server.attach_session(target_session=session_name)
        except LibTmuxException as exc:
            raise TmuxError(str(exc)) from exc

    # ------------------------------------------------------------------
    # Pane interaction
    # ------------------------------------------------------------------
    def send_keys(self, session_name: str, *keys: str, enter: bool = True, pane: str = "0") -> None:
        pane_obj = self._get_pane(session_name, pane)
        try:
            pane_obj.send_keys(*keys, enter=enter)
        except LibTmuxException as exc:
            raise TmuxError(str(exc)) from exc

    def capture_pane(
        self,
        session_name: str,
        *,
        pane: str = "0",
        scrollback: int | None = None,
    ) -> PaneCapture:
        pane_obj = self._get_pane(session_name, pane)
        try:
            lines = pane_obj.capture_pane(start=-abs(scrollback) if scrollback else None)
        except LibTmuxException as exc:
            raise TmuxError(str(exc)) from exc

        return PaneCapture(
            session=session_name,
            pane=pane,
            lines=lines,
            dead=self._is_pane_dead(pane_obj),
        )

    def iter_pane_lines(
        self,
        session_name: str,
        *,
        pane: str = "0",
        poll_interval: float = 0.5,
    ) -> Iterator[str]:
        pane_obj = self._get_pane(session_name, pane)
        previous: List[str] = []

        while True:
            try:
                current = pane_obj.capture_pane()
            except LibTmuxException as exc:
                raise TmuxError(str(exc)) from exc

            for idx, line in enumerate(current):
                if idx >= len(previous) or previous[idx] != line:
                    yield line

            if self._is_pane_dead(pane_obj):
                break
            if not self.session_exists(session_name):
                break
            previous = current
            time.sleep(poll_interval)

    def wait_for_session_end(
        self,
        session_name: str,
        *,
        timeout: Optional[float] = None,
        poll_interval: float = 0.5,
    ) -> bool:
        start = time.monotonic()
        while self.session_exists(session_name):
            if timeout is not None and time.monotonic() - start >= timeout:
                return False
            time.sleep(poll_interval)
        return True

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _find_session(self, session_name: str):
        try:
            self._server.list_sessions()
            return self._server.find_where({"session_name": session_name})
        except LibTmuxException as exc:
            message = str(exc)
            if "no server running" in message:
                return None
            raise TmuxError(message) from exc

    def _get_pane(self, session_name: str, pane: str) -> Pane:
        session = None
        deadline = time.monotonic() + self._spawn_timeout
        while time.monotonic() < deadline:
            session = self._find_session(session_name)
            if session is not None:
                break
            time.sleep(self._spawn_poll_interval)

        if session is None:
            raise TmuxError(f"tmux session '{session_name}' not found")

        try:
            window = session.attached_window or session.list_windows()[0]
            panes = window.list_panes()
        except LibTmuxException as exc:
            raise TmuxError(str(exc)) from exc

        pane_index = int(pane)
        if pane_index >= len(panes):
            raise TmuxError(f"pane index {pane} invalid for session '{session_name}'")

        return panes[pane_index]

    @staticmethod
    def _is_pane_dead(pane: Pane) -> bool:
        return pane.get("pane_dead") == "1"

    def _cmd(self, *args: str) -> Any:
        try:
            result = self._server.cmd(*args)
        except LibTmuxException as exc:
            raise TmuxError(str(exc)) from exc
        return result
