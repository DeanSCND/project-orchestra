# GitHub Organization Guide

## How Project Orchestra is Organized

GitHub has **three separate but connected systems** for organizing work:

---

## 1. Issues (Task Tracking)

**What:** Individual tasks with descriptions, labels, and assignments  
**Where:** https://github.com/DeanSCND/project-orchestra/issues

### Current Issues
- **21 issues total** (#1-21)
- Each issue has:
  - Title and description
  - Priority label (P0, P1, P2)
  - Component label (backend, frontend, infrastructure)
  - Time estimate
  - Acceptance criteria
  - Assigned to a milestone

### Example Issue Structure
```
Issue #16: Task Router - Intelligent Task Classification
Priority: P0
Labels: backend, P0
Milestone: Milestone 2
Estimate: 8 hours
Status: Open
```

### How to Work with Issues
```bash
# List all issues
gh issue list

# View specific issue
gh issue view 16

# Create new issue
gh issue create --title "..." --body "..."

# Close completed issue
gh issue close 16
```

---

## 2. Milestones (Time-Based Grouping)

**What:** Collections of issues grouped by delivery timeframe  
**Where:** https://github.com/DeanSCND/project-orchestra/milestones

### Current Milestones

#### Milestone 1: PoC - Primary Agent Interface (9 issues)
- Due: January 31, 2025
- Focus: Basic infrastructure
- Issues: #1-9

#### Milestone 2: Multi-Agent Orchestration (12 issues)
- Due: February 14, 2025
- Focus: Delegation and routing
- Issues: #10-21

#### Milestone 3: Production Security (0 issues)
- Due: February 28, 2025
- Focus: Auth0, Twingate, hardening
- Issues: TBD

#### Milestone 4: Advanced Features (0 issues)
- Due: March 14, 2025
- Focus: Grid view, telemetry
- Issues: TBD

#### Milestone 5: Production Ready (0 issues)
- Due: March 31, 2025
- Focus: Docker, CI/CD, monitoring
- Issues: TBD

### Milestone Status
```bash
# View milestone progress
gh api repos/DeanSCND/project-orchestra/milestones/1

# List issues in milestone
gh issue list --milestone "Milestone 1: PoC - Primary Agent Interface"
```

---

## 3. Projects (Visual Board)

**What:** Kanban-style board to visualize work across milestones  
**Where:** https://github.com/users/DeanSCND/projects/13

### Project: "Project Orchestra Development"
- **Status:** All 21 issues now linked
- **View:** Kanban board with columns
- **Default columns:** 
  - Todo
  - In Progress
  - Done

### How Projects Differ from Milestones

**Milestones:**
- Time-based (Week 1, Week 2, etc.)
- Deadline-oriented
- Fixed grouping

**Projects:**
- Status-based (Todo, In Progress, Done)
- Workflow-oriented
- Dynamic (drag & drop)

### Using the Project Board

1. **View all work:** https://github.com/users/DeanSCND/projects/13
2. **Drag issues** between columns as you work
3. **Filter by milestone** to see specific timeframe
4. **Track progress** visually

### Customizing the Board

You can add custom columns:
- Todo
- In Progress
- In Review
- Blocked
- Done

Or use different views:
- Kanban (default)
- Table
- Roadmap (timeline view)

---

## How They Work Together

```
Issue #16: Task Router
    ↓ belongs to
Milestone 2: Multi-Agent Orchestration
    ↓ tracked in
Project: Orchestra Development (Kanban board)
    ↓ current status
Column: Todo
```

### Workflow Example

**Starting new work:**
```bash
# 1. Pick issue from milestone
gh issue list --milestone "Milestone 1"

# 2. Assign to yourself
gh issue edit 1 --add-assignee @me

# 3. Move to "In Progress" on project board
# (Do this manually on GitHub UI, or via API)

# 4. Work on the issue
git checkout -b issue-1-monorepo-setup
# ... make changes ...

# 5. Create PR and link issue
gh pr create --title "Setup monorepo #1"

# 6. After merge, close issue
gh issue close 1

# 7. Issue automatically moves to "Done" on project board
```

---

## Current Organization Status

### ✅ Completed
- [x] 5 milestones created
- [x] 21 issues created and assigned to milestones
- [x] Project board created
- [x] All issues linked to project board
- [x] Labels created (P0, P1, P2, backend, frontend, etc.)

### 📋 Next Steps

**After merging PR #22 and #23:**

1. **Run milestone reorganization:**
   ```bash
   ./scripts/reorganize-milestones.sh
   ```
   This will:
   - Create "TRUE MVP - Week 1" milestone
   - Create 7 new issues for Week 1
   - Update existing issues with deferral notices

2. **Start working:**
   - Go to Project board: https://github.com/users/DeanSCND/projects/13
   - Filter by "TRUE MVP - Week 1" milestone
   - Pick first issue (#23 or similar)
   - Move to "In Progress"
   - Start building!

---

## Helpful Commands

### Issues
```bash
# List open issues
gh issue list

# List by milestone
gh issue list --milestone "Milestone 1"

# List by label
gh issue list --label P0

# View issue details
gh issue view 16

# Create issue
gh issue create --title "New feature" --body "Description"

# Close issue
gh issue close 16
```

### Milestones
```bash
# List milestones
gh api repos/DeanSCND/project-orchestra/milestones --jq '.[] | "\(.number): \(.title) - \(.open_issues) open"'

# Create milestone
gh api repos/DeanSCND/project-orchestra/milestones -X POST \
  -f title="New Milestone" \
  -f due_on="2025-02-28T00:00:00Z"
```

### Projects
```bash
# List projects
gh project list --owner @me

# Add issue to project
gh project item-add 13 --owner @me --url https://github.com/DeanSCND/project-orchestra/issues/1

# View project
# (Use web UI - better experience)
# https://github.com/users/DeanSCND/projects/13
```

---

## Visual Hierarchy

```
Repository: project-orchestra
│
├── Issues (#1-21)
│   ├── #1: Monorepo setup
│   ├── #2: FastAPI WebSocket
│   └── ... (19 more)
│
├── Milestones (5 total)
│   ├── Milestone 1 (9 issues)
│   ├── Milestone 2 (12 issues)
│   ├── Milestone 3 (0 issues)
│   ├── Milestone 4 (0 issues)
│   └── Milestone 5 (0 issues)
│
└── Projects (1 board)
    └── Orchestra Development (21 issues)
        ├── Todo
        ├── In Progress
        └── Done
```

---

## Best Practices

### 1. One Issue = One Task
- Keep issues focused
- Break large work into multiple issues
- Each issue should be completable in 1-8 hours

### 2. Use Milestones for Timeline
- Milestones represent deadlines
- Group related work by delivery time
- Don't move issues between milestones unless plans change

### 3. Use Project Board for Daily Work
- Move issues as you work on them
- "In Progress" = currently working
- "Blocked" = waiting on something
- "Done" = merged and deployed

### 4. Link PRs to Issues
```bash
# In PR description or commit message
Closes #16
Fixes #16
Resolves #16
```

This automatically closes the issue when PR is merged.

### 5. Keep Issues Updated
- Comment with progress
- Update labels if priority changes
- Mention blockers
- Link related issues

---

## Your Current View

**Issues:** https://github.com/DeanSCND/project-orchestra/issues  
**Milestones:** https://github.com/DeanSCND/project-orchestra/milestones  
**Project Board:** https://github.com/users/DeanSCND/projects/13

All 21 issues are now visible in the project board and organized by milestones!

---

## FAQ

**Q: Why is the project board empty-looking?**  
A: It starts with default columns. All issues are in "Todo" until you move them. Once you start working, drag issues to "In Progress" and "Done".

**Q: How do I customize the board?**  
A: Go to the project settings (gear icon) and add/remove columns, or change to Table/Roadmap view.

**Q: Can I have multiple project boards?**  
A: Yes! You could create separate boards for:
- Backend work
- Frontend work
- Documentation
- etc.

**Q: Do I need to use all three (issues, milestones, projects)?**  
A: Technically no, but they serve different purposes:
- **Issues:** Track individual tasks (required)
- **Milestones:** Track deadlines (optional but helpful)
- **Projects:** Visualize workflow (optional but great for daily work)

---

**The project board is now fully set up and ready to use!** 🎼
