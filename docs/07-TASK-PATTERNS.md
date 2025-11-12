# Task Routing Patterns - 9 Months of Learnings

**Based on real-world usage of Claude Code, Droid, Cursor, and Aider**

## Pattern Matrix

| Task Type | Best Tool | Best Model | Avg Cost | Why |
|-----------|-----------|------------|----------|-----|
| Code Review | GPT-4o-mini | gpt-4o-mini | $0.20 | Fast, catches obvious issues, cheap |
| Architecture Planning | Claude Code | claude-opus | $2-5 | Best reasoning, sees big picture |
| UI Components | Cursor | claude-sonnet | $1-2 | Excellent React/Tailwind understanding |
| Backend APIs | Droid | claude-sonnet | $1-3 | Handles FastAPI/Django patterns well |
| Long Refactors | Droid | claude-opus | $3-8 | Maintains context across many files |
| Git Operations | Aider | gpt-4o | $0.50-1 | Native git integration, commit messages |
| Simple Bugs | O3-mini | o3-mini | $0.10-0.30 | Fast, cheap, good for obvious fixes |
| Test Writing | GPT-4o-mini | gpt-4o-mini | $0.30-0.80 | Follows patterns well, cheap |
| Documentation | GPT-4o-mini | gpt-4o-mini | $0.15-0.40 | Clear writing, low complexity |
| Database Schema | Droid | claude-sonnet | $1-2 | Good at migrations and relationships |

## Cost Tiers

### Tier 1: Ultra-Cheap ($0.10-0.50)
**Models:** gpt-4o-mini, o3-mini  
**Use for:**
- Code reviews (obvious issues)
- Documentation updates
- Simple bug fixes
- Test writing
- Variable/function renaming

**When NOT to use:**
- Architecture decisions
- Complex refactors
- Novel problems

### Tier 2: Mid-Range ($1-3)
**Models:** claude-sonnet, gpt-4o  
**Use for:**
- UI component implementation
- API endpoints
- Database migrations
- Integration work
- Most CRUD operations

**Best ROI tier** - handles 80% of tasks effectively

### Tier 3: Premium ($3-8)
**Models:** claude-opus, gpt-4.5  
**Use for:**
- System architecture
- Complex algorithms
- Long refactors (10+ files)
- Novel problem solving
- Performance optimization

**Use sparingly** - reserve for tasks that actually need this power

## Real-World Patterns

### Pattern 1: CRUD Feature Development

```yaml
feature: "User Management CRUD"
breakdown:
  - task: "Database schema and migrations"
    tool: droid
    model: claude-sonnet
    cost_estimate: $1.50
    
  - task: "FastAPI endpoints (CRUD)"
    tool: droid
    model: claude-sonnet
    cost_estimate: $1.80
    
  - task: "React components (List, Form, Detail)"
    tool: cursor
    model: claude-sonnet
    cost_estimate: $1.20
    
  - task: "Integration tests"
    tool: aider
    model: gpt-4o-mini
    cost_estimate: $0.40
    
total_estimate: $4.90
parallel_time: ~10 min
sequential_time: ~25 min
savings: 60% time, 30% cost vs all-Opus
```

### Pattern 2: Bug Fix → Test → Deploy

```yaml
workflow: "Fix production bug"
steps:
  - task: "Identify and fix bug"
    tool: o3-mini  # Fast, good for obvious bugs
    model: o3-mini
    cost: $0.20
    
  - task: "Add regression test"
    tool: aider  # Best for git/test workflow
    model: gpt-4o-mini
    cost: $0.30
    
  - task: "Review changes and commit"
    tool: aider
    model: gpt-4o-mini
    cost: $0.10
    
total: $0.60
time: 3-5 min
```

### Pattern 3: Full Feature with Architecture

```yaml
feature: "Add OAuth2 authentication"
phases:
  architecture:
    tool: claude-code  # Plan with human in loop
    model: claude-opus
    cost: $3.00
    output: architecture.md
    
  implementation:
    - backend:
        tool: droid
        model: claude-sonnet
        cost: $2.50
        
    - frontend:
        tool: cursor
        model: claude-sonnet
        cost: $1.80
        
    - tests:
        tool: aider
        model: gpt-4o-mini
        cost: $0.60
        
  review:
    tool: claude-code
    model: claude-opus
    cost: $1.50
    
total: $9.40
time: ~30 min (with review cycles)
value: Production-ready OAuth2 implementation
```

## Anti-Patterns (What NOT to Do)

### ❌ Anti-Pattern 1: Using Opus for Everything
```yaml
# BAD - Costs $15 for simple task
task: "Rename getUserById to fetchUserById"
tool: claude-code
model: claude-opus  # Overkill!
cost: $0.80
```

```yaml
# GOOD - Same result, 90% cheaper
task: "Rename getUserById to fetchUserById"
tool: o3-mini
model: o3-mini
cost: $0.08
```

### ❌ Anti-Pattern 2: Sequential When Parallel Works
```yaml
# BAD - 30 minutes total
backend: "Build API" → 10 min
frontend: "Build UI" → 10 min (waits for backend)
tests: "Write tests" → 10 min (waits for frontend)
```

```yaml
# GOOD - 10 minutes total
all: [backend, frontend, tests]  # Run in parallel
integration: "Wire together" → 2 min
```

### ❌ Anti-Pattern 3: Wrong Tool for Task
```yaml
# BAD - Droid isn't great at UI
task: "Build responsive navbar with animations"
tool: droid  # Wrong choice!
result: Functional but not idiomatic React
```

```yaml
# GOOD - Cursor excels at UI
task: "Build responsive navbar with animations"
tool: cursor
result: Beautiful, idiomatic React with Tailwind
```

## Decision Tree

```
Task arrives
│
├─ Is it a bug fix?
│  ├─ Yes, obvious? → o3-mini
│  └─ Yes, complex? → claude-sonnet
│
├─ Is it UI work?
│  └─ Yes → cursor (claude-sonnet)
│
├─ Is it backend API?
│  └─ Yes → droid (claude-sonnet)
│
├─ Is it git/commit related?
│  └─ Yes → aider
│
├─ Does it need architecture thinking?
│  └─ Yes → claude-code (claude-opus)
│
├─ Is it refactoring >10 files?
│  └─ Yes → droid (claude-opus)
│
└─ Is it simple/repetitive?
   └─ Yes → gpt-4o-mini
```

## Escape Hatches

### When Routing Fails
1. **Tool unavailable** → Fallback to primary agent (Claude Code)
2. **Cost exceeded** → Prompt human for approval
3. **Task unclear** → Route to Claude Code for clarification
4. **Multiple tool match** → Default to cheapest option
5. **Tool fails** → Retry once, then escalate to human

### Manual Override
```bash
# Force specific tool regardless of routing
orchestra delegate --force-tool droid --task "..."

# Set cost ceiling
orchestra delegate --max-cost 2.00 --task "..."

# Disable routing (always use primary)
orchestra delegate --no-routing --task "..."
```

## Validation Metrics

Track these to tune routing over time:

```python
metrics = {
    "routing_accuracy": 0.85,  # 85% of routes were optimal
    "cost_savings": 0.68,      # 68% cheaper than all-Opus
    "time_savings": 0.55,      # 55% faster via parallelism
    "human_interventions": 0.12 # Only 12% needed manual override
}
```

## Tool-Specific Quirks

### Claude Code
- **Strength:** Architecture, reasoning, explaining
- **Weakness:** Can be verbose, slower
- **Best for:** Planning phase, final review

### Droid
- **Strength:** Long context, backend patterns
- **Weakness:** UI/frontend work
- **Best for:** API development, refactoring

### Cursor
- **Strength:** UI components, modern React/Tailwind
- **Weakness:** Backend logic
- **Best for:** Frontend implementation

### Aider
- **Strength:** Git integration, commit messages
- **Weakness:** Large architectural changes
- **Best for:** Incremental changes, test writing

### O3-mini
- **Strength:** Speed, cost efficiency
- **Weakness:** Novel problems, complex reasoning
- **Best for:** Simple fixes, repetitive tasks

## Cost Reality Check

**Monthly usage (heavy AI coding):**
- Without Orchestra: ~$300-500/month (using Opus for everything)
- With Orchestra: ~$100-150/month (smart routing)
- **Savings: $200-350/month** (60-70% reduction)

**Break-even:** First month of use pays for development time

---

**Document Status:** Living document  
**Last Updated:** January 2025  
**Based on:** 9 months real usage  
**Update Frequency:** Monthly based on new patterns
