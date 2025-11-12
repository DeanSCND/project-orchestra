"""Command-line entry points for controlling local tmux sessions and delegations."""

from __future__ import annotations

import shlex
import time
from pathlib import Path
from typing import Iterable, Optional

from uuid import uuid4

import click

from .config import OrchestraConfig, load_config
from .run_history import RunHistory
from .summary import summarise
from .task_router import detect_category
from .tmux_manager import PaneCapture, TmuxError, TmuxManager


def _build_manager(tmux_binary: str | None) -> TmuxManager:
    return TmuxManager(tmux_binary or "tmux")


@click.group()
@click.option("--tmux", "tmux_binary", default="tmux", show_default=True, help="tmux binary to invoke")
@click.option(
    "--config",
    "config_path",
    type=click.Path(exists=False, dir_okay=False, path_type=Path),
    help="Path to orchestra configuration file",
)
@click.pass_context
def cli(ctx: click.Context, tmux_binary: str, config_path: Path | None) -> None:
    """Orchestra developer CLI."""

    manager = _build_manager(tmux_binary)
    try:
        config = load_config(config_path)
    except FileNotFoundError as exc:
        raise click.ClickException(f"Configuration file not found: {exc}") from exc

    ctx.obj = {"manager": manager, "config": config}
@cli.command()
@click.option("--from", "primary", default="claude", show_default=True, help="Primary agent name")
@click.option("--to", "secondary", default="auto", show_default=True, help="Secondary agent name or 'auto'")
@click.option("--task", "task_description", required=True, help="Task description to delegate")
@click.option("--wait", default=5.0, show_default=True, help="Seconds to wait before capturing output (ignored in follow mode)")
@click.option("--follow/--no-follow", default=False, show_default=True, help="Stream secondary output until the session exits")
@click.option("--follow-interval", default=1.0, show_default=True, help="Polling interval when following output")
@click.option("--cleanup/--no-cleanup", default=False, show_default=True, help="Kill tmux sessions after completion")
@click.pass_context
def delegate(
    ctx: click.Context,
    primary: str,
    secondary: str,
    task_description: str,
    wait: float,
    follow: bool,
    follow_interval: float,
    cleanup: bool,
) -> None:
    """Delegate a task from the primary agent to a secondary agent."""

    manager: TmuxManager = ctx.obj["manager"]
    config: OrchestraConfig = ctx.obj["config"]
    history = RunHistory()

    if any(ch in task_description for ch in ("\n", "\r")):
        raise click.ClickException("Task description must be a single line message")

    try:
        active_sessions = [name for name in manager.list_sessions() if name.startswith("run-")]
    except TmuxError:
        active_sessions = []

    if active_sessions:
        raise click.ClickException(
            "Another delegation run appears to be active: " + ", ".join(active_sessions)
        )

    primary_key = primary.lower()
    try:
        primary_wrapper = config.wrapper_for(primary_key)
    except KeyError as exc:
        raise click.ClickException(str(exc)) from exc

    if secondary.lower() == "auto":
        category = detect_category(task_description)
        secondary_key = config.select_tool(category)
        click.echo(f"Auto-selected secondary agent '{secondary_key}'")
    else:
        secondary_key = secondary.lower()

    try:
        secondary_wrapper = config.wrapper_for(secondary_key)
    except KeyError as exc:
        raise click.ClickException(str(exc)) from exc

    run_id = uuid4().hex[:8]
    primary_session = f"run-{run_id}-primary-{primary_key}"
    secondary_session = f"run-{run_id}-secondary-{secondary_key}"

    def build_command(wrapper: Path, *, agent: str, role: str) -> list[str]:
        return [
            "env",
            f"ORCHESTRA_RUN_ID={run_id}",
            f"ORCHESTRA_AGENT={agent}",
            f"ORCHESTRA_ROLE={role}",
            str(wrapper),
            task_description,
        ]

    history.start_run(
        run_id,
        task=task_description,
        primary=primary_key,
        secondary=secondary_key,
        primary_session=primary_session,
        secondary_session=secondary_session,
        cleanup=cleanup,
        follow_mode=follow,
    )

    click.echo(f"Run ID: {run_id}")
    click.echo(f"Spawning primary session '{primary_session}'")
    manager.spawn_session(
        primary_session,
        command=build_command(primary_wrapper, agent=primary_key, role="primary"),
        kill_existing=True,
    )

    click.echo(f"Spawning secondary session '{secondary_session}'")
    manager.spawn_session(
        secondary_session,
        command=build_command(secondary_wrapper, agent=secondary_key, role="secondary"),
        kill_existing=True,
    )

    capture: Optional[PaneCapture] = None
    task_summary_dict: dict | None = None
    streamed_lines: list[str] = []

    if follow:
        click.echo("Streaming output (Ctrl+C to abort)...")
        try:
            for line in manager.iter_pane_lines(
                secondary_session,
                poll_interval=max(0.1, follow_interval),
            ):
                if line.strip():
                    click.echo(f"    {line}")
                    streamed_lines.append(line)
        except KeyboardInterrupt:
            click.echo("\nStreaming interrupted by user")
        except TmuxError as exc:
            click.echo(f"\nStreaming stopped: {exc}", err=True)
        finally:
            try:
                capture = manager.capture_pane(secondary_session)
            except TmuxError:
                capture = None
    else:
        if wait > 0:
            time.sleep(wait)
        try:
            capture = manager.capture_pane(secondary_session)
        except TmuxError as exc:
            raise click.ClickException(str(exc)) from exc

    try:
        if capture is None:
            if streamed_lines:
                summary_lines = streamed_lines
            else:
                click.echo("No output captured from secondary agent")
                summary_lines = []
        else:
            summary_lines = capture.lines

        summary = summarise(summary_lines)
        task_summary_dict = {
            "status": summary.status,
            "files_modified": summary.files_modified,
            "details": summary.details,
        }

        click.echo("\nSummary:")
        click.echo(f"  Status: {summary.status}")
        click.echo(f"  Files modified: {summary.files_modified}")
        if summary.details:
            click.echo("  Recent output:")
            for line in summary.details:
                click.echo(f"    {line}")

        history.complete_run(run_id, status=summary.status, summary=task_summary_dict)
    except Exception:
        history.complete_run(run_id, status="failed", summary=task_summary_dict)
        raise
    finally:
        if cleanup:
            try:
                manager.kill_session(primary_session)
            except TmuxError:
                pass
            try:
                manager.kill_session(secondary_session)
            except TmuxError:
                pass



@cli.group()
@click.pass_context
def tmux(ctx: click.Context) -> None:  # noqa: D401
    """Manage tmux sessions used by Orchestra."""


@tmux.command("spawn")
@click.argument("session_name")
@click.option("--command", "command_str", help="Command to run when the session starts")
@click.option("--cwd", type=click.Path(exists=True, file_okay=False, path_type=str), help="Working directory for the session")
@click.option("--force", is_flag=True, help="Kill any existing session with the same name before creating a new one")
@click.pass_context
def tmux_spawn(ctx: click.Context, session_name: str, command_str: str | None, cwd: str | None, force: bool) -> None:
    manager: TmuxManager = ctx.obj["manager"]
    command: Iterable[str] | None = shlex.split(command_str) if command_str else None

    try:
        manager.spawn_session(session_name, command, start_directory=cwd, kill_existing=force)
    except TmuxError as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"Created tmux session '{session_name}'")


@tmux.command("send")
@click.argument("session_name")
@click.argument("keys", nargs=-1, required=True)
@click.option("--no-enter", is_flag=True, help="Do not send an implicit Enter keystroke after the provided keys")
@click.option("--pane", default="0", show_default=True, help="Pane index to target inside the session")
@click.option("--raw", is_flag=True, help="Send each key as provided without inserting spaces between tokens")
@click.pass_context
def tmux_send(
    ctx: click.Context,
    session_name: str,
    keys: tuple[str, ...],
    no_enter: bool,
    pane: str,
    raw: bool,
) -> None:
    manager: TmuxManager = ctx.obj["manager"]

    try:
        payload = keys if raw else (" ".join(keys),)
        manager.send_keys(session_name, *payload, enter=not no_enter, pane=pane)
    except TmuxError as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"Sent keys to '{session_name}:{pane}'")


@tmux.command("capture")
@click.argument("session_name")
@click.option("--pane", default="0", show_default=True, help="Pane index to capture")
@click.option("--scrollback", type=int, help="Number of lines of scrollback to include (negative values are clamped)")
@click.pass_context
def tmux_capture(ctx: click.Context, session_name: str, pane: str, scrollback: int | None) -> None:
    manager: TmuxManager = ctx.obj["manager"]

    try:
        capture: PaneCapture = manager.capture_pane(session_name, pane=pane, scrollback=scrollback)
    except TmuxError as exc:
        raise click.ClickException(str(exc)) from exc

    for line in capture.lines:
        click.echo(line)


@tmux.command("list")
@click.pass_context
def tmux_list(ctx: click.Context) -> None:
    manager: TmuxManager = ctx.obj["manager"]
    try:
        sessions = manager.list_sessions()
    except TmuxError as exc:
        raise click.ClickException(str(exc)) from exc

    if not sessions:
        click.echo("No tmux sessions found")
        return

    for session in sessions:
        click.echo(session)


@tmux.command("kill")
@click.argument("session_name")
@click.pass_context
def tmux_kill(ctx: click.Context, session_name: str) -> None:
    manager: TmuxManager = ctx.obj["manager"]
    try:
        manager.kill_session(session_name)
    except TmuxError as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"Killed tmux session '{session_name}'")


@tmux.command("attach")
@click.argument("session_name")
@click.pass_context
def tmux_attach(ctx: click.Context, session_name: str) -> None:
    manager: TmuxManager = ctx.obj["manager"]

    if not manager.session_exists(session_name):
        raise click.ClickException(f"Session '{session_name}' does not exist")

    click.echo(f"Attaching to {session_name} (Ctrl+B D to detach)")
    manager.attach_session(session_name)


@cli.group()
@click.pass_context
def run(ctx: click.Context) -> None:  # noqa: D401
    """Inspect stored delegate runs."""


@run.command("list")
@click.option("--limit", default=10, show_default=True, help="Number of recent runs to display")
@click.pass_context
def run_list(ctx: click.Context, limit: int) -> None:
    history = RunHistory()
    runs = history.list_runs(limit=limit)
    if not runs:
        click.echo("No runs recorded yet")
        return

    for entry in runs:
        primary = entry.get("primary", "?")
        secondary = entry.get("secondary", "?")
        status = entry.get("status", "unknown")
        started = entry.get("started_at", "")
        completed = entry.get("completed_at") or "in-progress"
        task = entry.get("task", "")
        if len(task) > 60:
            task = task[:57] + "..."
        click.echo(
            f"{entry['run_id']}  {status:<10}  {primary}->{secondary}  {started}  {completed}  {task}"
        )


@run.command("attach")
@click.argument("run_id")
@click.option("--role", type=click.Choice(["primary", "secondary"]), default="secondary", show_default=True)
@click.pass_context
def run_attach(ctx: click.Context, run_id: str, role: str) -> None:
    history = RunHistory()
    record = history.get_run(run_id)
    if not record:
        raise click.ClickException(f"Run '{run_id}' not found")

    session_name = record.get(f"{role}_session")
    if not session_name:
        raise click.ClickException(f"Run '{run_id}' is missing a session name for role '{role}'")

    manager: TmuxManager = ctx.obj["manager"]
    if not manager.session_exists(session_name):
        raise click.ClickException(
            f"Session '{session_name}' is not active. Rerun with --no-cleanup to keep sessions alive."
        )

    click.echo(f"Attaching to {session_name} ({role})")
    manager.attach_session(session_name)


if __name__ == "__main__":
    cli()
