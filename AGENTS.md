# Agent Instructions

You are a capable assistant working on this project.

**Session Start Rule (Important):**  
At the start of **every new session**, first read the file `.grok/memory.md`.  
This loads the project memory index and the rules for the modular memory system.  
Treat the contents of `.grok/memory.md` as active context for the entire session.

---

## Modular Memory System

We use a hierarchical memory system:

- `.grok/memory.md` is the **lightweight index** (read this first on every new session).
- Detailed information is stored in separate files inside `.grok/memory/`.
- Only read specific memory files (`tools.md`, `user-preferences.md`, `important-decisions.md`) when you actually need the information.

### Memory Files Overview:
- `tools.md` — Tools, methods, frameworks, and resources
- `user-preferences.md` — Working style, preferences, and rules
- `important-decisions.md` — Important decisions (see strict rules below)

---

## Important Decisions Rules (Critical)

The file `important-decisions.md` must be maintained with these strict rules:

1. **Reverse Chronological Order** — Always add new decisions at the **top** of the file.
2. **Date Format** — Every decision must start with: `**YYYY-MM-DD** — Decision Title`
3. **Superseding Rule** — Newer decisions take precedence over older ones if contradictory.
4. **Clarification Rule** — If a new decision contradicts an existing one, **ask the user for clarification** before finalizing the update.

Example format:
```markdown
**2026-05-18** — Switched from Approach A to Approach B because...

**2026-05-10** — Decided to use X instead of Y (superseded on 2026-05-18)
```

---

## General Memory Rules

- Keep `.grok/memory.md` lightweight and up to date.
- Create new memory files when a topic becomes too large.
- Always update the index (`.grok/memory.md`) when you create or significantly modify a linked file.
- After major work or decisions, perform a quick memory review and update.
- The hooks in `.grok/hooks/` provide additional automation (session timestamps + gentle reminders on Stop/PreCompact).