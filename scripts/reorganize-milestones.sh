#!/bin/bash
# Reorganize milestones based on simplified MVP approach

cd /home/dean/Development/RandD/project-orchestra

echo "🎯 Reorganizing milestones for TRUE MVP approach..."
echo ""

# Create new TRUE MVP milestone
echo "Creating TRUE MVP milestone (Week 1 only)..."
gh api repos/DeanSCND/project-orchestra/milestones -X POST \
  -f title="TRUE MVP - Week 1" \
  -f state="open" \
  -f description="Prove delegation works: Claude → Droid. CLI only, no web UI, no auth. 8-12 hours total." \
  -f due_on="2025-01-17T00:00:00Z"

echo ""
echo "✅ TRUE MVP milestone created"
echo ""

# Update original Milestone 1 description
echo "Updating Milestone 1 description (now Week 2-3)..."
gh api repos/DeanSCND/project-orchestra/milestones/1 -X PATCH \
  -f description="DEFERRED from TRUE MVP. Add web UI, real cost tracking, multiple agents. Only start after Week 1 MVP proven."

echo ""
echo "✅ Milestone 1 updated"
echo ""

# Add comment to all Milestone 1 issues
echo "Adding comments to Milestone 1 issues (marking as deferred)..."

for issue in 1 2 3 4 5 6 7 8 9; do
  gh issue comment $issue --body "## 📋 Milestone Reorganization

This issue has been **deferred from TRUE MVP** (Week 1).

**New plan:**
- **Week 1:** TRUE MVP milestone - Just prove delegation works (CLI only)
- **Week 2-3:** This issue (Milestone 1)

**Rationale:**
- Need to prove core value before building infrastructure
- Web UI/auth/WebSocket are polish, not core value
- Opus recommended: Start with absolute minimum

See \`docs/09-TRUE-MVP.md\` for Week 1 scope."
done

echo ""
echo "✅ All Milestone 1 issues updated"
echo ""

# Create placeholder issues for TRUE MVP
echo "Creating TRUE MVP issues..."

gh issue create \
  --title "TRUE MVP: Basic Tmux Manager" \
  --milestone "TRUE MVP - Week 1" \
  --label "P0,backend" \
  --body "## Objective
Create minimal tmux session manager using python-libtmux.

## Scope
- Spawn tmux session with command
- Capture pane output
- Kill session
- NO streaming, NO real-time updates

## Implementation
See \`docs/09-TRUE-MVP.md\` Step 1

**Estimate:** 2 hours"

gh issue create \
  --title "TRUE MVP: Simple Task Router" \
  --milestone "TRUE MVP - Week 1" \
  --label "P0,backend" \
  --body "## Objective
Pattern-based task routing (not ML, just regex).

## Scope
- Match patterns like 'react' → cursor
- Match 'api' → droid
- Default fallback

## Implementation
See \`docs/09-TRUE-MVP.md\` Step 2

**Estimate:** 1 hour"

gh issue create \
  --title "TRUE MVP: Output Parser & Summary" \
  --milestone "TRUE MVP - Week 1" \
  --label "P0,backend" \
  --body "## Objective
Parse tool output into structured summary.

## Scope
- Regex-based parsing (files modified, errors)
- Structured dataclass output
- NAIVE implementation (improve later)

## Implementation
See \`docs/09-TRUE-MVP.md\` Step 3

**Estimate:** 2 hours"

gh issue create \
  --title "TRUE MVP: CLI Entry Point" \
  --milestone "TRUE MVP - Week 1" \
  --label "P0,backend" \
  --body "## Objective
Click-based CLI for delegation command.

## Scope
\`\`\`bash
orchestra delegate --task \"...\" --to droid
\`\`\`

## Implementation
See \`docs/09-TRUE-MVP.md\` Step 4

**Estimate:** 2 hours"

gh issue create \
  --title "TRUE MVP: Tool Wrappers" \
  --milestone "TRUE MVP - Week 1" \
  --label "P0,backend" \
  --body "## Objective
Bash wrappers for Claude and Droid.

## Scope
- wrappers/claude.sh
- wrappers/droid.sh
- Standardized interface

## Implementation
See \`docs/09-TRUE-MVP.md\` Step 5

**Estimate:** 2 hours"

gh issue create \
  --title "TRUE MVP: Config File Loading" \
  --milestone "TRUE MVP - Week 1" \
  --label "P1,backend" \
  --body "## Objective
Load tool paths and routing from config.yaml.

## Implementation
See \`docs/09-TRUE-MVP.md\` Step 6

**Estimate:** 1 hour"

gh issue create \
  --title "TRUE MVP: End-to-End Testing" \
  --milestone "TRUE MVP - Week 1" \
  --label "P0,backend" \
  --body "## Objective
Test full delegation flow with REAL Claude and Droid.

## Success Criteria
\`\`\`bash
./orchestra delegate --task \"Create User model\"
# Output: Works, shows summary, tmux sessions created/cleaned
\`\`\`

**Estimate:** 2 hours"

echo ""
echo "✅ TRUE MVP issues created"
echo ""
echo "📊 Summary:"
echo "  - TRUE MVP milestone: Week 1 (8-12 hours)"
echo "  - 7 new issues created for TRUE MVP"
echo "  - Original Milestone 1 issues deferred to Week 2-3"
echo "  - All stakeholders notified via issue comments"
echo ""
echo "View milestones: https://github.com/DeanSCND/project-orchestra/milestones"
echo "View issues: https://github.com/DeanSCND/project-orchestra/issues"
