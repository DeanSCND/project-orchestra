import json
import os
import subprocess
import sys
from pathlib import Path


CLI_MODULE = "orchestra.cli"


def run_cli(args, *, env=None, timeout=60):
    final_env = os.environ.copy()
    if env:
        final_env.update(env)
    return subprocess.run(
        [sys.executable, "-m", CLI_MODULE, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
        env=final_env,
    )


def test_delegate_codex_flow(tmp_path: Path):
    state_dir = tmp_path / "state"
    env = {
        "ORCHESTRA_STATE_DIR": str(state_dir),
        "ORCHESTRA_TMUX_SPAWN_TIMEOUT": "3",
    }

    result = run_cli(
        [
            "delegate",
            "--from",
            "claude",
            "--to",
            "codex",
            "--task",
            "Generate hello world",
            "--wait",
            "0.2",
            "--cleanup",
        ],
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert "Summary:" in result.stdout
    assert "codex" in result.stdout

    history_file = state_dir / "runs.json"
    assert history_file.exists()
    data = json.loads(history_file.read_text())
    assert data
    latest = data[-1]
    assert latest["secondary"] == "codex"
    assert latest["status"] in {"completed", "unknown"}


def test_task_validation(tmp_path: Path):
    env = {"ORCHESTRA_STATE_DIR": str(tmp_path / "state")}
    result = run_cli(
        [
            "delegate",
            "--task",
            "Line1\nLine2",
        ],
        env=env,
    )

    assert result.returncode != 0
    assert "single line" in result.stderr.lower()
