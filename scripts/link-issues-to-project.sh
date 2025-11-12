#!/bin/bash
# Link all issues to GitHub Project board

cd /home/dean/Development/RandD/project-orchestra

PROJECT_NUMBER=13
OWNER="@me"
REPO_URL="https://github.com/DeanSCND/project-orchestra"

echo "🔗 Linking all issues to Project #${PROJECT_NUMBER}..."
echo ""

# Get all issue numbers
ISSUE_NUMBERS=$(gh issue list --limit 100 --json number --jq '.[].number')

for issue_num in $ISSUE_NUMBERS; do
    echo "Adding issue #${issue_num}..."
    gh project item-add ${PROJECT_NUMBER} --owner ${OWNER} --url "${REPO_URL}/issues/${issue_num}" 2>/dev/null
done

echo ""
echo "✅ All issues linked to project board!"
echo "View project: https://github.com/users/DeanSCND/projects/13"
