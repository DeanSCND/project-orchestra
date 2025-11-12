# The TRUE MVP - Week 1 Only

**Goal:** Prove delegation works. ONE primary agent delegates to ONE secondary agent. That's it.

## What We're Building

A single Python script that:
1. Spawns Claude Code in tmux
2. Claude delegates a task to Droid
3. Droid completes task
4. Summary returned to Claude
5. You observe via `tmux attach`

**No web UI. No auth. No WebSocket. No database.**

## Success Criteria

```bash
# This should work by end of Week 1:
./orchestra delegate \
  --from claude \
  --to droid \
  --task "Add a User model to FastAPI with CRUD endpoints"

# Expected output:
# ✅ Spawned Claude in tmux session 'primary'
# ✅ Claude analyzed task
# ✅ Spawned Droid in tmux session 'secondary-1'
# ✅ Droid completed task (3 files modified)
# ✅ Summary returned to Claude
# 💰 Cost: $1.80
# ⏱️  Time: 8 minutes
```

## Implementation (8-12 hours)

### File Structure
```
orchestra/
├── cli.py           # Entry point
├── tmux_manager.py  # Spawn/capture tmux sessions
├── task_parser.py   # Simple pattern matching
├── summary.py       # Parse output → structured summary
├── config.yaml      # Tool paths and API keys
└── wrappers/
    ├── claude.sh    # Wrapper for Claude Code
    └── droid.sh     # Wrapper for Droid
```

### Step 1: Tmux Manager (2 hours)

```python
# orchestra/tmux_manager.py
import libtmux

class TmuxManager:
    def __init__(self):
        self.server = libtmux.Server()
    
    def spawn_session(self, name: str, command: str):
        """Spawn new tmux session with command."""
        session = self.server.new_session(
            session_name=name,
            window_command=command
        )
        return session
    
    def capture_output(self, session_name: str) -> str:
        """Capture pane output from session."""
        session = self.server.find_where({"session_name": session_name})
        pane = session.attached_window.attached_pane
        return pane.capture_pane()
    
    def kill_session(self, session_name: str):
        """Kill tmux session."""
        session = self.server.find_where({"session_name": session_name})
        session.kill_session()
```

### Step 2: Simple Task Router (1 hour)

```python
# orchestra/task_parser.py
import re

PATTERNS = {
    "ui": ["react", "component", "frontend", "tailwind"],
    "backend": ["api", "endpoint", "fastapi", "database"],
    "git": ["commit", "merge", "branch"],
}

def route_task(task_description: str) -> str:
    """Simple pattern matching for task routing."""
    task_lower = task_description.lower()
    
    # Check UI patterns
    if any(p in task_lower for p in PATTERNS["ui"]):
        return "cursor"
    
    # Check backend patterns
    if any(p in task_lower for p in PATTERNS["backend"]):
        return "droid"
    
    # Check git patterns
    if any(p in task_lower for p in PATTERNS["git"]):
        return "aider"
    
    # Default fallback
    return "droid"
```

### Step 3: Summary Parser (2 hours)

```python
# orchestra/summary.py
import re
from dataclasses import dataclass

@dataclass
class TaskSummary:
    status: str
    files_modified: int
    duration_sec: int
    errors: list[str]
    
def parse_output_to_summary(output: str) -> TaskSummary:
    """
    Parse raw tool output into structured summary.
    This is NAIVE parsing - just enough for MVP.
    """
    # Count files modified
    files = re.findall(r'modified: (.*?\.py)', output)
    
    # Check for errors
    errors = re.findall(r'ERROR: (.*)', output)
    
    # Estimate duration (placeholder)
    duration = 300  # 5 min default
    
    # Determine status
    status = "failed" if errors else "completed"
    
    return TaskSummary(
        status=status,
        files_modified=len(files),
        duration_sec=duration,
        errors=errors
    )
```

### Step 4: CLI Entry Point (2 hours)

```python
# orchestra/cli.py
import click
from orchestra.tmux_manager import TmuxManager
from orchestra.task_parser import route_task
from orchestra.summary import parse_output_to_summary
import time

@click.group()
def cli():
    """Orchestra CLI - Minimal MVP"""
    pass

@cli.command()
@click.option('--from', 'primary', default='claude', help='Primary agent')
@click.option('--to', 'secondary', default='auto', help='Secondary agent or auto')
@click.option('--task', required=True, help='Task description')
def delegate(primary: str, secondary: str, task: str):
    """Delegate task from primary to secondary agent."""
    
    click.echo(f"🎼 Orchestra MVP - Delegating task...")
    
    # Auto-route if needed
    if secondary == 'auto':
        secondary = route_task(task)
        click.echo(f"📍 Auto-routed to: {secondary}")
    
    # Initialize tmux manager
    tmux = TmuxManager()
    
    # Spawn primary agent (Claude)
    click.echo(f"✅ Spawning {primary}...")
    primary_session = tmux.spawn_session(
        name="primary",
        command=f"./wrappers/{primary}.sh"
    )
    
    # Wait for Claude to analyze (simulate for MVP)
    time.sleep(2)
    
    # Spawn secondary agent
    click.echo(f"✅ Spawning {secondary}...")
    secondary_session = tmux.spawn_session(
        name="secondary-1",
        command=f"./wrappers/{secondary}.sh '{task}'"
    )
    
    # Wait for completion (naive - just wait fixed time)
    click.echo(f"⏳ Waiting for {secondary} to complete...")
    time.sleep(60)  # 1 min for MVP
    
    # Capture output
    output = tmux.capture_output("secondary-1")
    
    # Parse to summary
    summary = parse_output_to_summary(output)
    
    # Display results
    click.echo(f"\n✅ Task completed!")
    click.echo(f"   Status: {summary.status}")
    click.echo(f"   Files modified: {summary.files_modified}")
    click.echo(f"   Duration: {summary.duration_sec}s")
    
    if summary.errors:
        click.echo(f"   ⚠️  Errors: {len(summary.errors)}")
        for error in summary.errors:
            click.echo(f"      - {error}")
    
    # Cleanup
    tmux.kill_session("primary")
    tmux.kill_session("secondary-1")

if __name__ == '__main__':
    cli()
```

### Step 5: Tool Wrappers (2 hours)

```bash
#!/bin/bash
# wrappers/claude.sh
# Minimal Claude Code wrapper

echo "🤖 Claude Code starting..."
echo "Task: $1"

# For MVP, just echo. Real version would call claude-code
echo "Analyzing task..."
sleep 2
echo "Delegating to secondary agent..."
```

```bash
#!/bin/bash
# wrappers/droid.sh
# Minimal Droid wrapper

TASK="$1"

echo "🤖 Droid starting..."
echo "Task: $TASK"

# For MVP, simulate work
echo "Creating files..."
sleep 5
echo "modified: models/user.py"
echo "modified: routers/users.py"
echo "modified: schemas/user.py"
echo "✅ Completed!"
```

### Step 6: Config File (1 hour)

```yaml
# config.yaml
tools:
  claude:
    path: /usr/local/bin/claude-code
    wrapper: ./wrappers/claude.sh
    api_key_env: ANTHROPIC_API_KEY
  
  droid:
    path: /usr/local/bin/droid
    wrapper: ./wrappers/droid.sh
    api_key_env: FACTORY_TOKEN
  
  cursor:
    path: /usr/local/bin/cursor-agent
    wrapper: ./wrappers/cursor.sh
    api_key_env: CURSOR_API_KEY
  
  aider:
    path: /usr/local/bin/aider
    wrapper: ./wrappers/aider.sh
    api_key_env: OPENAI_API_KEY

routing:
  ui: cursor
  backend: droid
  git: aider
  default: droid
```

---

## Testing the MVP

### Test 1: Manual Delegation
```bash
# Start primary agent manually
tmux new-session -s primary -d "bash"
tmux send-keys -t primary "echo 'Claude Code here'" C-m

# Start secondary agent
tmux new-session -s secondary -d "bash"
tmux send-keys -t secondary "echo 'Droid here'" C-m

# Capture output
tmux capture-pane -t secondary -p

# Cleanup
tmux kill-session -t primary
tmux kill-session -t secondary
```

### Test 2: Via CLI
```bash
# Simple task
./orchestra delegate --task "Create User model"

# Explicit routing
./orchestra delegate --from claude --to droid --task "Build API"

# Auto-routing
./orchestra delegate --to auto --task "Create React navbar"
# Should auto-route to cursor
```

---

## What's NOT in MVP

- ❌ Web UI (use `tmux attach` to watch)
- ❌ Auth0 / JWT (local only, trust localhost)
- ❌ WebSocket streaming (capture output post-facto)
- ❌ Database (no persistence)
- ❌ Cost tracking (hardcode estimates)
- ❌ Multiple secondaries (just one for now)
- ❌ Parallel execution (sequential is fine)
- ❌ Error recovery (manual restart)
- ❌ Real-time updates (poll tmux pane)

---

## Success Looks Like

**Day 1-2:** Basic tmux spawning works
**Day 3-4:** Can capture output and parse simple summary
**Day 5:** CLI works end-to-end for one delegation
**Day 6-7:** Test with REAL Claude and Droid, fix issues

**End of Week 1:**
```bash
$ ./orchestra delegate --task "Add authentication to FastAPI"
🎼 Orchestra MVP - Delegating task...
📍 Auto-routed to: droid
✅ Spawning claude...
✅ Spawning droid...
⏳ Waiting for droid to complete...

✅ Task completed!
   Status: completed
   Files modified: 5
   Duration: 480s
   Cost: $1.80

# You can now view full output:
$ tmux attach -t secondary-1
```

**Validation:** If this works, the CORE VALUE is proven. Everything else is polish.

---

## What Comes After MVP

**Week 2: Make it useful**
- Add real cost tracking
- Better output parsing
- Support 2-3 concurrent secondaries
- Basic config file loading

**Week 3: Make it observable**
- Simple web UI (just terminal viewing)
- WebSocket streaming
- Basic task status

**Week 4+: Make it production-ready**
- Auth (Twingate + Auth0)
- Error recovery
- Full task router
- Summary protocol refinement

---

## Why This Approach Works

1. **Proves core value immediately** - Delegation works or doesn't
2. **No infrastructure complexity** - Just Python + tmux
3. **Easy to debug** - `tmux attach` shows everything
4. **Rapid iteration** - Change code, test in seconds
5. **Forces simplicity** - Can't hide behind fancy UI

If this MVP doesn't work by end of Week 1, the project isn't viable.  
If it DOES work, everything else is just improving the UX.

**The hard part isn't the web UI - it's making delegation actually work.**

---

**Build this first. Everything else can wait.**
