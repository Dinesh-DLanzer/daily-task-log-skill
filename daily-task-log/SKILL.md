---
name: daily-task-log
description: Write or update the daily task log (a `daily-tasks/` folder with one DD-MM-YYYY sub-folder per day, a readme summary per day, and one file per time slot named by its timeline). Use when the user says "daily-task-log", "daily task sheet", "log today's work", "update yesterday's tasks", or asks what was done on a day with correct timestamps.
license: MIT
metadata:
  version: "1.0"
---

# daily-task-log

Keep a local, human-readable record of what was done each day, grouped into time slots.

Trigger it by name in a prompt, for example: "use the daily-task-log skill for today" or "daily-task-log: add yesterday".

## Output layout

```
daily-tasks/
  readme.md                         summary table of all days (newest last)
  DD-MM-YYYY/
    readme.md                       summary of that day + slot table + open items
    HH-MM-AM-to-HH-MM-PM.md         one file per time slot (12-hour clock, zero padded)
```

Example slot file name: `11-35-AM-to-12-20-PM.md`. A slot that crosses midnight is split into two files.
Templates are in `templates/`; `scripts/new_day.py` scaffolds a day from them. `<skill dir>` is the folder holding this SKILL.md. Create the root folder in the current project (or the path the user gives).

## Steps

1. **Pick the day(s).** Default is today in the user's local time. Accept "yesterday", a date, or a range. Use `DD-MM-YYYY` for folder names.
2. **Settle the timezone.** Run `date` and use the machine's local zone. If the user states a zone or corrects the times, use that and write it in the readme (`Times are IST`). Servers often run on a different clock than the user, so convert any server timestamps and say so.
3. **Collect evidence. Never invent work.**
   - Git: `python3 <skill dir>/scripts/git_timeline.py YYYY-MM-DD` (add `--all` for every branch, `--gap N` to tune slot splitting) prints that day's commits in local time, grouped into clusters, with a suggested slot file name for each.
   - Agent sessions: use the current session's own history, and other transcripts if the tool keeps them (for Claude Code: `~/.claude/projects/<project>/*.jsonl`, each line has a `timestamp` in UTC).
   - Anything the user tells you: work done outside git, outside the editor, or on servers.
4. **Build time slots.** Start from the clusters, then adjust with session start and end times. Prefer 1 to 5 slots a day. If the user gives a start and end time for the day, the first slot starts there and the last ends there. Mark estimated boundaries with `~` and say they are estimates.
5. **Write the slot files** from `templates/slot.md`: a short timeline, what was done as checkboxes, findings, and anything not finished. Describe what each commit or action does. Do not claim who typed what when several agents or people committed.
6. **Write the day readme** from `templates/day-readme.md`: a one-paragraph summary, the slot table with links, the outcome, and open items.
7. **Update `daily-tasks/readme.md`**: add or update the row for each day, keeping the table in date order.
8. **Keep it private by default.** Add `daily-tasks/` to `.gitignore` if it isn't there, unless the user wants it committed. Never commit unless asked.
9. **Tell the user** which files were written, where the times came from, which boundaries are estimates, and what you could not confirm.

## Rules

- No secrets: never write passwords, tokens, keys, connection strings or private keys into the log, even if they appeared in the session.
- Times come from evidence (commit times, transcript timestamps, server logs, what the user said). If a gap has no evidence, say so instead of filling it.
- Commit time is when work was saved, not when it started. Say that once in the day readme.
- Don't overwrite a day the user has edited without reading it first. Add to it or ask.
- Keep slot files short and factual. Link, don't paste long outputs.
