#!/usr/bin/env python3
"""
Stop + PreCompact hook for the modular memory system.

Emits a gentle reminder (via additionalInstructions) encouraging the agent
to record important decisions or facts in the memory files.

We deliberately do NOT fire this on PostToolUse / every tool call because
routine actions (ls, pwd, reading files, etc.) would trigger it far too often.
"""

import json
import sys


REMINDER_TEXT = (
    "Consider updating the memory system (especially important-decisions.md) "
    "if you learned anything important during this work. "
    "PreCompact is an especially good moment to capture decisions before context is summarized."
)


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
        "post_tool_use": "PostToolUse",
        "posttooluse": "PostToolUse",
        "stop": "Stop",
        "pre_compact": "PreCompact",
        "precompact": "PreCompact",
        "pre-compact": "PreCompact",
        "task_completed": "TaskCompleted",
        "taskcompleted": "TaskCompleted",
        "session_end": "SessionEnd",
        "session_start": "SessionStart",
    }
    return mapping.get(name, raw_name)


def main():
    try:
        raw = json.load(sys.stdin)
    except Exception:
        raw = {}

    event_name = normalize_event_name(raw)

    # Only remind on meaningful completion points, not on every individual tool call.
    # Stop = agent finished thinking / responding
    # PreCompact = context is about to be summarized (excellent moment to capture decisions)
    if event_name in ("Stop", "PreCompact"):
        print(json.dumps({
            "additionalInstructions": REMINDER_TEXT,
            "event": "MemoryReminder"
        }))

    # Always succeed — this is a non-blocking, passive reminder hook.
    sys.exit(0)


if __name__ == "__main__":
    main()