"""Simple run history persistence for the Orchestra CLI."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional


STATE_DIR = Path.home() / ".cache" / "project-orchestra"
RUN_HISTORY_FILE = STATE_DIR / "runs.json"
MAX_RUNS = 50


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class RunRecord:
    run_id: str
    task: str
    primary: str
    secondary: str
    started_at: str
    status: str
    primary_session: str
    secondary_session: str
    cleanup: bool
    follow_mode: bool
    summary: Optional[Dict] = None
    completed_at: Optional[str] = None


class RunHistory:
    def __init__(self, path: Path = RUN_HISTORY_FILE) -> None:
        self._path = path

    # ------------------------------------------------------------------
    # CRUD helpers
    # ------------------------------------------------------------------
    def start_run(
        self,
        run_id: str,
        *,
        task: str,
        primary: str,
        secondary: str,
        primary_session: str,
        secondary_session: str,
        cleanup: bool,
        follow_mode: bool,
    ) -> None:
        record = RunRecord(
            run_id=run_id,
            task=task,
            primary=primary,
            secondary=secondary,
            started_at=_utcnow_iso(),
            status="running",
            primary_session=primary_session,
            secondary_session=secondary_session,
            cleanup=cleanup,
            follow_mode=follow_mode,
        )
        self._persist(record)

    def complete_run(
        self,
        run_id: str,
        *,
        status: str,
        summary: Optional[Dict] = None,
    ) -> None:
        runs = self._read()
        for entry in runs:
            if entry["run_id"] == run_id:
                entry["status"] = status
                entry["summary"] = summary
                entry["completed_at"] = _utcnow_iso()
                break
        else:
            # No existing run, create a minimal record so we don't lose the event.
            runs.append(
                {
                    "run_id": run_id,
                    "task": "",
                    "primary": "",
                    "secondary": "",
                    "started_at": _utcnow_iso(),
                    "status": status,
                    "primary_session": "",
                    "secondary_session": "",
                    "cleanup": True,
                    "follow_mode": False,
                    "summary": summary,
                    "completed_at": _utcnow_iso(),
                }
            )
        self._write(runs)

    def list_runs(self, *, limit: int = 10) -> List[Dict]:
        runs = self._read()
        runs.sort(key=lambda item: item.get("started_at", ""), reverse=True)
        return runs[:limit]

    def get_run(self, run_id: str) -> Optional[Dict]:
        runs = self._read()
        for entry in runs:
            if entry["run_id"] == run_id:
                return entry
        return None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _persist(self, record: RunRecord) -> None:
        runs = self._read()
        runs = [entry for entry in runs if entry["run_id"] != record.run_id]
        runs.append(asdict(record))
        self._write(runs)

    def _read(self) -> List[Dict]:
        if not self._path.exists():
            return []
        try:
            with self._path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
                if isinstance(data, list):
                    return data
        except json.JSONDecodeError:
            pass
        return []

    def _write(self, runs: Iterable[Dict]) -> None:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        runs_list = list(runs)
        if len(runs_list) > MAX_RUNS:
            runs_list = sorted(runs_list, key=lambda item: item.get("started_at", ""), reverse=True)[:MAX_RUNS]
        with self._path.open("w", encoding="utf-8") as handle:
            json.dump(runs_list, handle, indent=2)
