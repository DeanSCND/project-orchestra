"""Parse tmux output from agent runs into coarse summaries."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class TaskSummary:
    status: str
    files_modified: int
    details: List[str]


SUCCESS_PATTERNS = (
    re.compile(r"\bcompleted\b", re.IGNORECASE),
    re.compile(r"✅"),
    re.compile(r'"event"\s*:\s*"task_completed"'),
)

ERROR_PATTERNS = (
    re.compile(r"\berror\b", re.IGNORECASE),
    re.compile(r"\bfailed\b", re.IGNORECASE),
)

FILE_PATTERN = re.compile(r"modified:\s+(?P<path>.+)")


def summarise(lines: Iterable[str]) -> TaskSummary:
    material = list(lines)
    joined = "\n".join(material)

    if any(pattern.search(joined) for pattern in ERROR_PATTERNS):
        status = "failed"
    elif any(pattern.search(joined) for pattern in SUCCESS_PATTERNS):
        status = "completed"
    else:
        status = "unknown"

    files = FILE_PATTERN.findall(joined)

    non_empty = [line for line in material if line.strip()]
    recent = (non_empty[-10:] or material[-10:]) if material else []

    return TaskSummary(status=status, files_modified=len(files), details=recent)
