# Grok Modular Memory System

A clean, hierarchical memory system for [Grok Build](https://grok.x.ai) that keeps long-term context lightweight while still giving the model rich, structured access to your project's knowledge.

## Why This Exists

Grok's built-in cross-session memory is powerful, but many users want **more control** over what gets remembered and how. This project gives you:

- A **lightweight index** that is automatically injected at the start of every session
- **Detailed memory files** that are only loaded when needed
- Strong conventions around **important decisions** (reverse chronological, explicit superseding rules)
- Automatic reminders at good moments (`Stop` and especially `PreCompact`)

The result is a memory system that scales well even on long-running projects without bloating every context window.

## Features

- **SessionStart hook** — Automatically loads `.grok/memory.md` and teaches the model how to use the modular system
- **SessionEnd hook** — Records when you stopped working
- **Smart reminders** — Only fires on `Stop` and `PreCompact` (not on every single tool call)
- **Strict decision tracking** — New decisions go at the top, newer decisions supersede older ones
- **AGENTS.md** — Project rules that are automatically loaded

## Directory Structure

```
.grok/
├── memory.md                 # Lightweight index (always loaded)
├── AGENTS.md                 # Project rules + memory system instructions
├── hooks/
│   ├── hooks.json            # Hook registration
│   ├── session-start.py      # Injects memory index
│   ├── session-end.py        # Records session end timestamp
│   └── memory-reminder.py    # Gentle reminder on Stop / PreCompact
└── memory/
    ├── tools.md
    ├── user-preferences.md
    └── important-decisions.md
```

## Quick Setup

### 1. Copy this structure into your project

The easiest way is to clone this repository and copy the `.grok/` folder into your own project.

### 2. Trust the hooks

In a Grok Build session, run:

```bash
/hooks-trust
```

Then reload hooks (`Ctrl+L` → `l`).

### 3. Start using it

From your next session onward, Grok will automatically see your memory index and follow the rules defined in `AGENTS.md`.

## The Modular Memory Philosophy

The core idea is **progressive disclosure**:

1. `.grok/memory.md` is small and is loaded on every session.
2. The detailed files in `.grok/memory/` are only read when the model actually needs them.
3. This keeps token usage low while still giving excellent long-term recall.

## Important Decisions File (Critical Rules)

The file `.grok/memory/important-decisions.md` follows strict conventions:

- **Reverse chronological order** — newest decisions at the top
- Every entry starts with `**YYYY-MM-DD** — Title`
- Newer decisions **supersede** older contradictory ones
- If a new decision would contradict an existing one, the model is instructed to **ask you for clarification** first

This creates a clean, auditable decision log over the life of a project.

## Recommended Workflow

- After any significant architectural or technical decision → update `important-decisions.md`
- Periodically review `.grok/memory.md` and the linked files
- Before major compaction (`PreCompact`), the system gently reminds you to capture anything important

## Customization

You can extend this system easily:

- Add new files under `.grok/memory/` and link them from `memory.md`
- Modify the reminder text in `memory-reminder.py`
- Add more hooks (e.g., on `UserPromptSubmit` for very long sessions)

## Requirements

- Grok Build (the TUI)
- Python 3 (for the hook scripts)
- The project must be **trusted** for hooks (`/hooks-trust`)

## License

MIT — feel free to use this in your own projects.

---

**Made for people who build ambitious things with Grok and want their context to actually remember what matters.**