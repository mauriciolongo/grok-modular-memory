#!/usr/bin/env python3
"""
SessionEnd hook for the modular memory system.
Appends a timestamp to .grok/memory.md when the session finishes.
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def normalize_event_name(data: dict) -> str:
    """Return a normalized event name from either the standard hook payload or legacy format."""
    if not isinstance(data, dict):
        return ""

    raw_name = (
        data.get("hookEventName")
        or data.get("hook_event_name")
        or data.get("event")
    )
    if not raw_name:
        return ""

    name = str(raw_name).strip().lower()

    mapping = {
        "session_end": "SessionEnd",
        "sessionend": "SessionEnd",
        "end": "SessionEnd",
        "session_start": "SessionStart",
        "post_tool_use": "PostToolUse",
        "stop": "Stop",
    }
    return mapping.get(name, raw_name)


def main():
    try:
        raw = json.load(sys.stdin)
    except Exception:
        raw = {}

    event_name = normalize_event_name(raw)

    memory_file = Path(".grok/memory.md")

    if memory_file.exists():
        try:
            content = memory_file.read_text()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            updated = content.rstrip() + f"\n\n---\n**Last session ended:** {timestamp}\n"
            memory_file.write_text(updated)
        except Exception as e:
            # Fail open — never block session end
            print(json.dumps({"error": f"Failed to update memory: {e}"}))
            sys.exit(0)

    # Non-blocking hook — we can return a small status message.
    print(json.dumps({
        "message": "Project memory saved successfully",
        "event": "SessionEnd"
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()