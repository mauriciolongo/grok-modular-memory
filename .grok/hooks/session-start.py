#!/usr/bin/env python3
"""
SessionStart hook for the modular memory system.

NOTE (May 2026): As of current Grok Build versions, returning "additionalInstructions"
from a SessionStart hook is NOT injected into the model prompt by the platform.
This script is kept for forward compatibility.

The reliable method today is the static "Session Start Rule" placed in the
project's root AGENTS.md file.
"""

import json
import sys
from pathlib import Path


def normalize_event_name(data: dict) -> str:
    """Return a normalized event name from either the standard hook payload or legacy format."""
    if not isinstance(data, dict):
        return ""

    # Standard Grok/Claude hook protocol
    raw_name = (
        data.get("hookEventName")
        or data.get("hook_event_name")
        or data.get("event")
    )
    if not raw_name:
        return ""

    name = str(raw_name).strip().lower()

    # Map common variants to our internal names
    mapping = {
        "session_start": "SessionStart",
        "sessionstart": "SessionStart",
        "start": "SessionStart",
        "post_tool_use": "PostToolUse",
        "posttooluse": "PostToolUse",
        "stop": "Stop",
        "session_end": "SessionEnd",
        "sessionend": "SessionEnd",
        "task_completed": "TaskCompleted",
        "taskcompleted": "TaskCompleted",
    }
    return mapping.get(name, raw_name)


def main():
    try:
        raw = json.load(sys.stdin)
    except Exception:
        raw = {}

    event_name = normalize_event_name(raw)

    # We only really care that we were invoked for SessionStart (the hooks.json guarantees it),
    # but we still normalize for robustness / future direct invocation.
    if event_name and event_name != "SessionStart":
        # Still proceed — the registration ensures correctness, but don't fail hard.
        pass

    memory_file = Path(".grok/memory.md")

    if memory_file.exists():
        memory_content = memory_file.read_text()
    else:
        memory_content = "No previous memory found."

    instructions = f"""PROJECT MEMORY INDEX (loaded automatically):

{memory_content}

---

**MODULAR MEMORY INSTRUCTION:**
This system uses separate memory files to optimize context.
- Only read specific files (tools.md, user-preferences.md, important-decisions.md) when you need the details.
- Follow the rules in AGENTS.md, especially the Important Decisions rules (reverse chronological order, dates, and clarification when decisions conflict).
"""

    # Grok supports "additionalInstructions" on SessionStart to inject context.
    print(json.dumps({
        "additionalInstructions": instructions,
        "event": "SessionStart"
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()