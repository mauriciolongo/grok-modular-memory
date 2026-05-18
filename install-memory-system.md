# Install the Grok Modular Memory System

This guide will help you install a persistent, hierarchical memory system for your project that works reliably with the current version of Grok Build.

## What This Memory System Does

The goal is to give Grok reliable long-term memory across sessions without bloating every context window. It works like this:

- **Lightweight memory index** — A small file (`.grok/memory.md`) that is loaded at the start of every session.
- **Detailed memory files** — Larger files (tools, preferences, decisions) that Grok only reads when it actually needs them.
- **Strict decision tracking** — Important architectural and technical decisions are recorded in reverse chronological order with clear rules.
- **Gentle reminders** — The system reminds you to capture important information at good moments (`Stop` and before context compaction).

Because of current limitations in Grok Build, we cannot yet rely on local project hooks. This setup uses a **global hook registration** method that is confirmed to work today.

---

## Step 1: Configure Your Project’s Root `AGENTS.md`

This is the most important and reliable part of the system right now.

### If you do **not** have a root `AGENTS.md` file

Create a new file called `AGENTS.md` in the root of your project and paste the following content:

```markdown
# Agent Instructions

You are a capable assistant working on this project.

**Session Start Rule (Important):**  
At the start of **every new session**, first read the file `.grok/memory.md`.  
This loads the project memory index and the rules for the modular memory system.  
Treat the contents of `.grok/memory.md` as active context for the entire session.

---

## Modular Memory System

We use a hierarchical memory system:

- `.grok/memory.md` is the lightweight index.
- Detailed information is stored in separate files inside `.grok/memory/`.
- Only read specific memory files when you actually need the information.

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
```

### If you **already have** a root `AGENTS.md`

Open your existing `AGENTS.md` and insert the following block **at the very top**, right after the main heading (or at the beginning of the file):

```markdown
**Session Start Rule (Important):**  
At the start of **every new session**, first read the file `.grok/memory.md`.  
This loads the project memory index and the rules for the modular memory system.  
Treat the contents of `.grok/memory.md` as active context for the entire session.

---
```

> **Tip:** Place this rule near the top so it is one of the first things Grok sees when it loads your project rules.

---

## Step 2: Create the Memory Template Files

These are **not example files** — they are the actual templates that should exist in your project.

After you have created your root `AGENTS.md`, ask Grok the following (copy and paste):

> "Please create the following files in the `.grok/memory/` directory (these are the real templates, not examples):
> 1. `.grok/memory.md` (the main lightweight index)
> 2. `.grok/memory/important-decisions.md`
> 3. `.grok/memory/user-preferences.md`
> 4. `.grok/memory/tools.md`
>
> Initialize them with sensible starter content following the Grok Modular Memory System conventions. For `important-decisions.md`, start with an entry for today noting that the memory system was set up."

Grok should create the files with reasonable starter content. You can review and adjust them afterward.

### Recommended Starter Content

If you want Grok to generate high-quality initial content, you can append this to your prompt:

> "Use the following recommended starter content as a guide when creating the files:"

Below are good examples of what the files should look like after initial creation.

#### 1. `.grok/memory.md` (Lightweight Index)

```markdown
# Project Memory Index

**Last Updated:** 2026-05-18

## Overview
This is a flexible knowledge base for ongoing work and decision tracking.

## Linked Memory Files
These files contain detailed information. Only read them when needed to conserve context.

- [Tools & Methods](./memory/tools.md)
- [User Preferences](./memory/user-preferences.md)
- [Important Decisions](./memory/important-decisions.md)

**Guideline:** Check this index first. Only open specific files when you need the full details.
```

#### 2. `.grok/memory/important-decisions.md`

```markdown
# Important Decisions

**Last Updated:** 2026-05-18

**2026-05-18** — Initial setup of the Grok Modular Memory System for this project.
```

#### 3. `.grok/memory/user-preferences.md`

```markdown
# User Preferences

**Last Updated:** 2026-05-18

## Communication Style
- 

## Working Preferences
- 
```

#### 4. `.grok/memory/tools.md`

```markdown
# Tools & Methods

**Last Updated:** 2026-05-18

## Current Tools
- 

## Preferred Methods
- 
```

**Note to Grok:** Please adapt and expand these templates based on the actual project, its domain, and any context already known about the user or codebase.

---

### Expected Files After This Step

- `.grok/memory.md` — The lightweight index (should reference the other files)
- `.grok/memory/important-decisions.md` — For recording major decisions (must follow the strict reverse-chronological format)
- `.grok/memory/user-preferences.md` — Your personal working style and preferences
- `.grok/memory/tools.md` — Tools and methods you commonly use

---

## Step 3: Understand the Hooks (Please Read)

This memory system can optionally install two helper hooks that run automatically:

| Hook                  | What it does                                                              | Why it’s useful                                      |
|-----------------------|---------------------------------------------------------------------------|------------------------------------------------------|
| `session-end.py`      | Records when a session ends in `.grok/memory.md`                          | Helps track when you last worked on the project      |
| `memory-reminder.py`  | Gently reminds you to record decisions on `Stop` or before compaction     | Prevents losing good ideas and important decisions   |

**Important notes about these hooks:**

- They are registered **globally** (in `~/.grok/hooks/`). Once installed for one project, they can become active in other projects as well. This is expected behavior.
- **They do nothing** if the current project does not have a `.grok/memory.md` file. They are completely safe to have enabled across multiple projects.
- It is possible that suitable global hooks are **already installed** from a previous project where you activated this memory system. In that case, you may already see the hooks when you open the Hooks modal (`Ctrl + L`).
- `session-start.py` is **not** registered globally. At the moment Grok does not support injecting `additionalInstructions` from `SessionStart` hooks, so it is kept locally only for future compatibility.

**What Grok should say when asking about the hooks:**

When you reach this point, Grok should clearly explain the above points and then ask something like:

> “I see that you are setting up the memory system. The reminder and session tracking hooks need to be registered globally. This means they can become active in other projects too. However, they will do nothing unless the project has a `.grok/memory.md` file.  
> 
> I notice you may already have global hooks from another project. Would you like to:
> 1. Reuse the existing global hooks (recommended if they are already working), or
> 2. Create a fresh registration specifically for this project?”

**Do you want to proceed with the hooks?**

Please answer **yes** or **no** before continuing.

> **If you answer “no”**:  
> You can still use the memory system fully. You will simply need to manually prompt Grok at the start of sessions (or when relevant) to read `.grok/memory.md`, follow the rules in your `AGENTS.md`, and update `important-decisions.md` when you make important choices. Many people start this way and add the hooks later.

---

## Step 4: Install the Global Hooks (Only if you answered “yes”)

### 4.1 Create the global hooks directory using your project folder name

Run these commands while inside your project folder:

```bash
# Use your actual folder name (this is the standard convention)
PROJECT_SLUG=$(basename "$PWD")
mkdir -p ~/.grok/hooks/$PROJECT_SLUG
```

### 4.2 Copy the working hook scripts

```bash
cp .grok/hooks/session-end.py .grok/hooks/memory-reminder.py ~/.grok/hooks/$PROJECT_SLUG/
chmod +x ~/.grok/hooks/$PROJECT_SLUG/*.py
```

> Note: We are **not** copying `session-start.py` into the global registration at this time.

### 4.3 Create the global registration file

Create this file:

```
~/.grok/hooks/$PROJECT_SLUG.json
```

Paste the following content (you can ask Grok to generate it with the correct folder name filled in):

```json
{
  "description": "Modular Memory System hooks for PROJECT_SLUG",
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.grok/hooks/PROJECT_SLUG/session-end.py",
            "timeout": 5
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.grok/hooks/PROJECT_SLUG/memory-reminder.py",
            "timeout": 5
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.grok/hooks/PROJECT_SLUG/memory-reminder.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### 3.4 Verify the installation

```bash
ls -la ~/.grok/hooks/$PROJECT_SLUG/
ls -la ~/.grok/hooks/$PROJECT_SLUG.json
```

You should see `session-end.py` and `memory-reminder.py` inside the folder, plus the `.json` registration file next to it.

---

## Step 5: Activate the Hooks

1. Start or restart a Grok Build session in your project.
2. Open the Hooks modal: Press `Ctrl + L` (or type `/hooks`).
3. Press `l` (lowercase L) to **reload** all hooks.
4. You should now see the memory hooks listed.

---

## Verification

After setup, try these checks:

- Start a new session and ask:  
  *"Have you read the project memory index from `.grok/memory.md`?"*

- Work for a while, then stop the session. You should eventually see a reminder about recording important decisions.

- Close a session and later check that `.grok/memory.md` contains a “Last session ended” timestamp.

---

## Optional: Customize the Supplemental Memory Files

The memory system includes two additional template files that you can fill in over time:

- **`.grok/memory/user-preferences.md`** — Your working style, communication preferences, decision-making habits, etc.
- **`.grok/memory/tools.md`** — Tools, frameworks, libraries, and methods you commonly use.

These files are **not required** for the system to function. Many people start with just `.grok/memory.md` and `important-decisions.md`, then gradually populate the supplemental files as useful patterns emerge.

Grok will only read them when it needs the information, keeping context usage efficient.

---

## Next Steps

Once the files are created:

- Ask Grok to start using `.grok/memory/important-decisions.md` for any significant choices going forward.
- Keep `.grok/memory.md` as your lightweight index (update it when you add major new context).
- Let the system remind you before major context compaction (if you installed the hooks).

If you chose not to install the hooks, you can always come back to this file later and run the installation steps.

---

**Thank you for setting up the memory system!**  
This should make long-running work with Grok much more reliable over time.