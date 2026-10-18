---
name: short-notes
description: Write or edit the user's personal Markdown notes (command cheat sheets, setup steps, how-tos, concept notes, checklists) in their scannable bullet-and-code style, in English or Thai, at a chosen detail level (brief, medium, or detailed). Use whenever the user asks, in any language, to jot down, save, summarize into, add to, or rewrite a note or a notes .md file, even if they don't mention a style, level, or language. Not for project docs such as README, CHANGELOG, AGENTS.md, CLAUDE.md, SKILL.md, or docs/ pages.
argument-hint: "[brief|medium|detailed] [english|thai] [topic or file]"
---

# Markdown Notes

The user opens these notes later to find a command or fact fast: headings are how they search, code blocks are what they copy, and prose is noise. Every rule below serves that.

## 1. Pick language and detail level

| Level | Each section has | Example |
| --- | --- | --- |
| brief | heading + code; at most one short bullet, often none | `references/brief.md` |
| medium | + 1–3 bullets: what it does, when to use it, what each placeholder means | `references/medium.md` |
| detailed | + expected output, common errors with the fix, alternatives, `> [!WARNING]` for data loss, a final references section | `references/detailed.md` |

Language is English or Thai. In Thai, headings and bullets are Thai, but commands, code, flags, paths, and technical terms (branch, commit, container) stay English, the way Thai developers write.

- Given in the request or as slash-command arguments → use it ("short" → brief, "in detail" → detailed, whatever language the user writes in)
- Existing note → keep its language; when adding to it, also match its density
- Whatever is still unknown → ask before writing, both in one round if both are missing (AskUserQuestion if available)

Read the example for the chosen level before writing. All three are the same Git note, so diff them when unsure where one level ends; follow their structure in either language.

## 2. Write

Cover what was asked; skip loosely related extras (detailed may add alternatives for the same task).

### Structure

- A new file starts with one `# title`
- `##` per task, named by the goal ("Create a new branch", not "git switch") so Ctrl+F and the outline find it; `###` for a step inside that task; never skip a heading level
- Commands that differ by OS get one heading per platform (`## Windows — PowerShell`, `## macOS — zsh`)
- Sections in the order they're used (setup → daily use → cleanup); no intro paragraph, no closing summary, no emoji in headings
- Steps as `###` headings, not numbered lists: headings show in the outline, and code under them needs no indenting

### Code

- Fenced block with a language tag (`bash`, `powershell`, `zsh`, `conf`, `json`; `text` for output), one block per step
- Copy-paste ready: no `$ ` prompt, no output inside a command block
- Placeholders in UPPER_SNAKE: `SERVER_IP`, `BRANCH_NAME`

### Text

- Short `- ` bullets, never paragraphs; explain a term as `` `term` → meaning ``
- Backticks only for literal commands, values, and paths, never for whole sentences
- Table only when comparing items across two or more attributes
- A command that deletes, overwrites, or force-pushes shows its consequence at every level, in its heading or one bullet, so it never runs by surprise
- Caveats sit right under the command they apply to; a final caveats section holds only general ones

### Accuracy

These commands get pasted later without re-checking, so correctness beats brevity: when unsure of a flag or syntax, check `--help` or official docs instead of guessing, and never invent a URL.

## 3. Edit an existing note

- Adding: put it under the matching heading and follow that note's conventions (language, heading and placeholder style); leave the rest untouched
- Rewriting or condensing (only when asked): cut words, not facts. Keep every command, path, and link unless it's a duplicate; if something must go, list it in your reply so the user can veto

## 4. Save

- Use the path the user gives
- In the notes repo (a root `notes/` folder of `.md` files), a new note goes to `notes/<topic>.md` in kebab-case
- Anywhere else, ask where to save, or reply with the note in chat if that's all they wanted
