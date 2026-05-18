# Grok Modular Memory System

> A clean, hierarchical, and opinionated memory system for **Grok Build** that scales gracefully on long projects.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/mauriciolongo/grok-modular-memory?style=social)](https://github.com/mauriciolongo/grok-modular-memory/stargazers)

A lightweight but powerful memory architecture for Grok that uses progressive disclosure, strict decision tracking, and well-timed reminders so the model actually remembers what matters — without bloating every context.

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

## Quick Start (Recommended)

### Option A — Use as a Template (Best)

1. Click the green **"Use this template"** button on the [GitHub repo](https://github.com/mauriciolongo/grok-modular-memory) (or clone it directly).
2. Copy the entire `.grok/` folder into your own project.
3. In a **fresh** Grok Build session inside your project, run:

   ```bash
   /hooks-trust
   ```

4. Press `Ctrl + L`, then `l` to reload hooks.

### Option B — Manual Copy

Clone this repo and copy just the `.grok/` directory into your target project:

```bash
git clone https://github.com/mauriciolongo/grok-modular-memory.git
cp -r grok-modular-memory/.grok /path/to/your-project/
```

Then follow steps 3–4 above.

---

**That's it.** From the next session onward, Grok will automatically load your memory index and follow the decision-tracking rules.

## How to Test This System

The best way to validate the memory system is **not** by asking Grok to clone the repo inside a session.

### Recommended Testing Workflow

1. **Create a completely fresh test directory** (outside this repository):

   ```bash
   mkdir ~/test-grok-memory
   cd ~/test-grok-memory
   ```

2. **Copy only the `.grok/` folder** from this repo (or from a fresh clone):

   ```bash
   cp -r /path/to/grok-modular-memory/.grok .
   ```

3. **Start a brand new Grok Build session** in that folder (very important — do not continue an old session).

4. Run `/hooks-trust` and reload hooks (`Ctrl+L` → `l`).

5. **Run a structured test**:
   - Ask Grok to do some real work (refactor something, plan a feature, debug an issue).
   - Make at least one explicit decision and ask it to record it in `important-decisions.md`.
   - Do some trivial commands (`ls`, `cat`, etc.) to verify the reminder does **not** fire on every tool use.
   - Work until you see the `PreCompact` reminder (you can force compaction or just work long enough).
   - Start a second session later and verify that the memory index + recent decisions are still present.

6. **Verify behavior**:
   - The model should reference the memory rules without you reminding it.
   - `important-decisions.md` should be maintained in reverse chronological order.
   - Reminders should only appear at `Stop` and `PreCompact`, not on routine tool calls.

This approach gives you the most realistic signal about whether the system actually helps in practice.

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