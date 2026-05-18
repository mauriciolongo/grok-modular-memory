# Contributing to Grok Modular Memory

Thank you for your interest in improving the Grok Modular Memory System!

This project aims to provide a clean, opinionated, and battle-tested memory architecture that many Grok users can drop into their own projects.

## Ways to Contribute

### 1. Improve the Core System

- Better hook logic (more intelligent reminder timing, better event detection)
- Improved `AGENTS.md` instructions
- New useful memory files or patterns
- Better `.gitignore` or documentation

### 2. Improve Documentation & Onboarding

- Better README examples
- More testing scenarios
- Video walkthroughs or blog posts (very welcome)
- Translations (if demand appears)

### 3. Share Real-World Usage

The best contributions often come from people who have used this system on real, long-running projects. Feedback about what worked and what was annoying is extremely valuable.

## How to Use This as a Template in Your Projects

This repository is designed to be **used as a template**, not forked for most people.

**Recommended flow:**

1. Click **"Use this template"** on GitHub (creates your own copy).
2. Copy the `.grok/` directory into your actual project(s).
3. Customize the memory files (`user-preferences.md`, `tools.md`, `important-decisions.md`) for that specific project.
4. (Optional) Keep your own fork if you want to maintain project-specific improvements.

You are encouraged to adapt the hooks and instructions to your personal style.

## Pull Request Guidelines

- Keep changes focused and well-scoped.
- Update the README when behavior or structure changes meaningfully.
- Test your changes using the workflow described in the README ("How to Test This System").
- For larger changes, open an issue first to discuss the idea.

## Philosophy We Try to Follow

- **Less noise is better than more features** — We deliberately removed the `PostToolUse` reminder because it fired too often.
- **Progressive disclosure** — The model should only see detailed memory when it actually needs it.
- **Human in the loop on conflicts** — The system should ask the user when decisions would contradict previous ones.
- **PreCompact is sacred** — This is one of the highest-leverage moments to capture knowledge.

## Questions?

Open an issue or start a discussion. We're happy to help people adapt this system to their workflow.

---

Thanks for helping make long-term work with Grok more reliable and pleasant.