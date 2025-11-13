# Agent Operations Guide

This document captures the tooling, workflows, and project-specific conventions used by Droid agents when working on **Project Orchestra**. It focuses on the Graphite CLI workflow for stacking pull requests and records the current project context so future sessions can onboard quickly.

---

## 1. Graphite CLI (2025) Overview

Graphite (https://graphite.dev) is a Git-based workflow tool designed for stacking small, incremental pull requests. It integrates with GitHub, providing commands that orchestrate branch creation, PR submission, and stack management.

### 1.1 Installation

```bash
curl -fsSL https://cli.graphite.dev/install.sh | sh
# or with Homebrew
brew install graphiteapp/tap/graphite
```

After installing, authenticate with GitHub:

```bash
gt auth login
```

### 1.2 Core Concepts

- **Stack**: An ordered series of small branches (and PRs) that build on one another.
- **Stack Root**: The base branch of the stack (usually `master`).
- **Checkout**: Each branch is an incremental change; reviewers can approve small PRs while maintaining overall context.

### 1.3 Common Commands

| Command | Description |
|---------|-------------|
| `gt init` | Initializes Graphite in the repo (run once). |
| `gt stack create` | Interactively selects commits to form a stack. |
| `gt branch create <name>` | Creates a new branch stacked on the current branch. |
| `gt branch submit` | Submits the current branch as a GitHub PR. |
| `gt stack submit` | Submits all branches in the stack. |
| `gt stack status` | Views the current stack, dependencies, and review state. |
| `gt branch land` | Lands (merges) the branch and rebases descendants. |
| `gt stack land` | Lands the entire stack in order. |

Graphite automatically maintains parent/child relationships and rebases descendants when the parent changes, which is ideal for the “split PR” workflow requested by reviewers.

### 1.4 Recommended Workflow for Project Orchestra

1. **Start from `master`:**
   ```bash
   git checkout master
   git pull
   gt init  # once per repo
   ```

2. **Create the first slice (e.g., CLI work):**
   ```bash
   gt branch create feature/delegation-cli
   # edit files, run tests
   gt branch submit  # opens PR vs master
   ```

3. **Create subsequent slices stacked on the previous branch:**
   ```bash
   gt branch create feature/daemon --parent feature/delegation-cli
   # implement daemon, commit
   gt branch submit
   ```

4. **Monitor stack:**
   ```bash
   gt stack status
   ```

5. **Land (after approvals):**
   ```bash
   gt branch land  # or gt stack land for entire stack
   ```

6. **Resync if parent changes (e.g., review feedback):**
   ```bash
   gt stack sync
   ```

**Note:** Graphite will prompt for commit messages and PR titles; use the repo’s conventional prefix (e.g., “Add tmux-backed delegation CLI…”).

---

## 2. Project Orchestra Context (Nov 2025)

### 2.1 Branch Strategy

- Default branch: `master`
- Working integration branch: `simplify-mvp`
- Stacked feature branches (current focus):
  - `feature/delegation-cli` → merged (PR #28)
  - Upcoming: `feature/daemon`, `feature/web-ui`

### 2.2 Issue Tracking Snapshot

- Closed per review: Issues #2 (daemon), #3 (tmux manager), #4 (web UI) after first PR cycle.
- Follow-up security/auth tickets opened:
  - #25 **Secure daemon WebSocket authentication**
  - #26 **Re-enable Auth0 integration for web UI**

### 2.3 CLI Artifacts Added (PR #28)

- `orchestra/` package (CLI entrypoint, config loader, run history, tmux manager, task router, summary parser).
- `packages/agent-wrappers/` with executable wrappers for Claude, Droid, Cursor, Aider, and Codex; Codex wrapper optionally executes the real CLI when installed.
- `tests/test_delegate_cli.py` covering end-to-end delegation and validation.
- `requirements.txt` now includes `libtmux`, `filelock`, and `pytest`.

### 2.4 Pending Work for Next PRs

1. **FastAPI daemon split**
   - Extract from prior commit snapshot (`feature/full-mvp` tag) into its own Graphite branch.
   - Address reviewer concerns: strict token enforcement (later, per Issue #25), rate limiting, memory cleanup.

2. **Web UI shell**
   - Reintroduce Next.js code stripped from CLI PR.
   - Auth disabled for now; follow-up per Issue #26.

3. **Security & Hardening**
   - Input sanitization in CLI already added; double-check before landing daemon/web UI PRs.
   - Validate wrappers exist; ensure config loader surfaces clear errors (already implemented).

### 2.5 Testing Commands Recap

- CLI integration: `pytest tests/test_delegate_cli.py`
- Manual smoke: `python3 -m orchestra.cli delegate --task "Create User model" --cleanup`
- tmux sessions created with prefix `run-<id>`.

### 2.6 Environment Notes

- `ORCHESTRA_STATE_DIR`: overrides run history location (used in tests).
- `ORCHESTRA_TMUX_SPAWN_TIMEOUT` / `ORCHESTRA_TMUX_SPAWN_POLL_INTERVAL`: control tmux manager waits.
- `ORCHESTRA_DAEMON_ALLOW_INSECURE_WS`: set to `1`/`true` for local WebSocket testing without Auth0 (defaults to secure-only; requires caution).
- Codex wrapper checks for `codex` command on PATH; otherwise emits simulated output.

### 2.7 Sensitive Files

- `.env.example` files are not yet re-added; ensure future PRs do not accidentally store secrets. Helper scripts (e.g., Graphite) should use environment variables or local config.

---

## 3. Additional Agent Guidance

- **Docs**: Avoid modifying `docs/*.md` unless specifically requested; current untracked docs relate to future auth work.
- **Testing before PR**: Always run pytest and lint (if relevant) before submitting.
- **Commit Hygiene**: Keep commits scoped to their feature branch; Graphite stack expects clean, reviewable slices.
- **Future Sessions**: Review this file before new work to keep tooling in sync; update with new commands, scripts, or branch conventions as they evolve.

---

*Maintained by Droid agents for Project Orchestra (last updated Nov 2025).* 
