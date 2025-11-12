"""Configuration loading for the Orchestra MVP."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Mapping, Optional

import yaml


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"


@dataclass(frozen=True)
class ToolConfig:
    name: str
    wrapper: Path


@dataclass(frozen=True)
class OrchestraConfig:
    tools: Dict[str, ToolConfig]
    routing: Mapping[str, str]
    default_tool: str

    def wrapper_for(self, tool: str) -> Path:
        key = tool.lower()
        if key not in self.tools:
            raise KeyError(f"Unknown tool '{tool}'")
        return self.tools[key].wrapper

    def select_tool(self, category: Optional[str]) -> str:
        if category and category in self.routing:
            return self.routing[category]
        return self.default_tool


def load_config(path: Path | None = None) -> OrchestraConfig:
    config_path = path or DEFAULT_CONFIG_PATH
    with config_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}

    raw_tools = raw.get("tools", {})
    base_dir = config_path.parent
    tools: Dict[str, ToolConfig] = {
        name.lower(): ToolConfig(
            name=name.lower(),
            wrapper=_resolve_path(base_dir, values["wrapper"]),
        )
        for name, values in raw_tools.items()
    }

    routing = raw.get("routing", {})
    default_tool = routing.get("default") or next(iter(tools.keys()), "droid")

    return OrchestraConfig(tools=tools, routing=routing, default_tool=default_tool)


def _resolve_path(base_dir: Path, raw_path: str) -> Path:
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        resolved = (base_dir / candidate).resolve()
        if resolved.exists():
            return resolved
        project_root = base_dir.parent
        alt = (project_root / candidate).resolve()
        if alt.exists():
            return alt
        return resolved
    return candidate
