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

## Current Working State (as of May 2026)

**Important:** As of the current version of Grok Build, `SessionStart` hooks that return `additionalInstructions` are **not yet injected** into the model's prompt by the platform (this was confirmed during real testing in the `grok-memory-test` project).

### What works reliably today:
- Static instructions placed in the **root `AGENTS.md`** (this is the recommended approach)
- `SessionEnd` hook (records session timestamp)
- Memory reminders on `Stop` and `PreCompact`

### What is aspirational (for when the platform supports it):
- Dynamic injection via the `SessionStart` hook

The template is designed so it works **today** using the reliable static method, while keeping the hook infrastructure for the future.

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

## Installation

The easiest and most reliable way to set up the memory system is to use the dedicated installation guide.

### Recommended Workflow

1. Copy the `.grok/` folder from this repository into your project.
2. Open the file `install-memory-system.md` in your project.
3. In a Grok Build session, simply tell Grok:

   > "Please read and follow the instructions in `install-memory-system.md` to set up the modular memory system for this project."

Grok will guide you through the entire process (creating `AGENTS.md`, the memory files, and optionally installing the hooks).

**Important:** When following the guide, ask Grok to create any new files that are needed and to adapt their content and structure to match the specific requirements, domain, and context of your project (rather than using generic templates).

### Global Hooks Behavior

The reminder and session tracking hooks are registered **globally**. This means:

- Once activated for one project, they can become active in other projects as well (this is expected behavior).
- They are safe: the hooks do nothing if the current project does not have a `.grok/memory.md` file.
- When running setup in a new project, Grok should check for existing global hooks from other projects and clearly explain the situation (including that the hooks are harmless without a memory file) before asking how to proceed.

**Note on our original intention:**  
Creating globally registered hooks was not our original plan. We designed the system around local project hooks (stored in `.grok/hooks/`) for better isolation between projects. However, due to current limitations in the Grok Build TUI, reliable local project hook discovery is not yet supported. The global registration method is currently the only working mechanism available. We hope this will change soon as the application is updated and we can move back to the preferred local hook approach.

The full guide is here: **[install-memory-system.md](install-memory-system.md)**

---

### What the Guide Covers

- Creating the root `AGENTS.md` with the required "Session Start Rule"
- Creating the actual memory template files (`memory.md`, `important-decisions.md`, `user-preferences.md`, `tools.md`)
- Understanding current platform limitations
- Installing the working global hooks (with your explicit consent)
- Verification steps

We strongly recommend using the guided workflow above rather than trying to follow the instructions manually.

### Quick Overview

1. Copy the `.grok/` folder into your project.
2. Follow the steps in `install-memory-system.md` to configure your root `AGENTS.md`.
3. Optionally install the global hooks for automatic reminders and session tracking.

The local `SessionStart` hook is included in the template for future compatibility but is not registered globally at this time (see the install guide for details).

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

## Contributors & Acknowledgments

- **Mauricio Longo** – Creator and maintainer of the Grok Modular Memory System
- **Grok** (built by xAI) – Assisted with architecture, documentation, testing workflows, and iterative improvements to the system

---

**Made for people who build ambitious things with Grok and want their context to actually remember what matters.**