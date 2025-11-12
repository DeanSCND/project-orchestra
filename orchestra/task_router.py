"""Naive task routing heuristics for the MVP."""

from __future__ import annotations

from typing import Iterable


PATTERN_GROUPS: dict[str, tuple[str, ...]] = {
    "frontend": ("react", "component", "frontend", "tailwind", "css", "ui"),
    "backend": ("api", "endpoint", "fastapi", "database", "crud", "schema", "model"),
    "git": ("commit", "merge", "branch", "rebase"),
}

CATEGORY_TO_TOOL: dict[str, str] = {
    "frontend": "cursor",
    "backend": "droid",
    "git": "aider",
}


def detect_category(task_description: str) -> str | None:
    lowered = task_description.lower()
    for category, keywords in PATTERN_GROUPS.items():
        if any(keyword in lowered for keyword in keywords):
            return category
    return None


def auto_select_tool(task_description: str, *, fallbacks: Iterable[str]) -> str:
    category = detect_category(task_description)
    if category and category in CATEGORY_TO_TOOL:
        return CATEGORY_TO_TOOL[category]

    for fallback in fallbacks:
        return fallback

    raise ValueError("No tools available for routing")
