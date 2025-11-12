# Basic Delegation Example

## Scenario
Building a CRUD API with React frontend.

## Manual Approach (Before Orchestra)

**Steps:**
1. Open Claude Code terminal
2. "Build FastAPI CRUD endpoints for users"
3. Wait 10 minutes...
4. Review output, copy files
5. Open Cursor in new terminal
6. "Build React components for user management"  
7. Wait 8 minutes...
8. Manually wire frontend to backend
9. Open Aider in third terminal
10. "Write integration tests"
11. Wait 5 minutes...

**Results:**
- ⏱️ **Time:** 30+ minutes
- 💰 **Cost:** ~$5-8 (depending on models used)
- 🧠 **Mental overhead:** HIGH (3 tool switches, manual coordination, context copying)

---

## Orchestra Approach

**Single Configuration:**
```yaml
task:
  description: "Build user management feature with CRUD API and React UI"
  
  components:
    backend:
      agent: "droid"
      task: "FastAPI CRUD endpoints for User model (schema, router, dependencies)"
      max_cost: 2.00
      timeout: 600
    
    frontend:
      agent: "cursor"  
      task: "React components (UserList, UserForm, UserDetail, API client)"
      max_cost: 1.50
      timeout: 480
    
    tests:
      agent: "aider"
      task: "Integration tests covering full user management flow"
      max_cost: 0.50
      timeout: 300
```

**Execution:**
```bash
orchestra execute task.yaml --parallel
```

**What Happens:**
1. Task router analyzes each component
2. Spawns 3 tmux sessions (Droid, Cursor, Aider)
3. All agents work **in parallel**
4. Cost tracker monitors in real-time
5. Summary protocol returns high-level results
6. You monitor from web dashboard

**Results:**
- ⏱️ **Time:** 12 minutes (parallel execution)
- 💰 **Cost:** $3.20 (smart routing to cheaper models)
- 🧠 **Mental overhead:** ZERO (just monitor dashboard)

**Savings:**
- ⚡ **60% faster**
- 💰 **47% cheaper**
- 🧠 **Zero coordination overhead**

---

## Key Insights

### Why Parallel Works
- Backend, frontend, and tests are independent
- No coordination needed until integration
- Orchestra handles synchronization automatically

### Why Cost Savings
- Task router identified "simple CRUD" pattern
- Routed to cheaper models where appropriate
- Backend used mid-tier model (necessary complexity)
- Frontend used Cursor (best for UI)
- Tests used Aider (best for git integration)

### Summary Protocol in Action

**Without Summary (Bad):**
Primary agent sees 5000+ lines of:
```
> droid
Analyzing project structure...
Creating models/user.py...
[500 lines of implementation details]
Running tests...
[1000 lines of test output]
...
```
Context window: 90% full ❌

**With Summary (Good):**
Primary agent sees:
```json
{
  "task": "backend",
  "status": "completed",
  "changes": "3 files created: models/user.py, routers/users.py, schemas/user.py",
  "loc_added": 250,
  "tests": "15 tests passing",
  "cost": "$1.80",
  "duration": "8 minutes",
  "next_actions": ["integrate frontend", "deploy"]
}
```
Context window: 5% used ✅

---

## Real-World Impact

This example is based on actual usage after 9 months of AI-assisted development. The patterns Orchestra automates are:
1. **Task decomposition** - Breaking features into parallel work
2. **Tool selection** - Picking the right AI for each job
3. **Cost optimization** - Using cheap models where sufficient
4. **Coordination** - Managing handoffs and integration
5. **Monitoring** - Tracking progress and costs

All of this manual overhead **disappears** with Orchestra.
