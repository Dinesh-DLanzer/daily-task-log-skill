# daily-task-log

An agent skill that keeps a daily task sheet: a `daily-tasks/` folder with one `DD-MM-YYYY` folder per day, a summary readme for each day, and one file per time slot named by its timeline.

```
daily-tasks/
  readme.md                       summary of all days
  08-10-2026/
    readme.md                     summary of that day
    12-00-AM-to-02-10-AM.md
    09-45-AM-to-12-10-PM.md
  09-10-2026/
    readme.md
    11-35-AM-to-12-20-PM.md
```

The agent builds the slots from real evidence (git commit times, session timestamps, what you tell it), converts server clocks to your timezone, marks estimated boundaries, and never writes secrets into the log.

## Install (all agents on this machine)

```bash
git clone https://github.com/Dinesh-DLanzer/daily-task-log-skill.git
cd daily-task-log-skill
./install.sh          # symlinks into ~/.agents, ~/.claude, ~/.codex, ~/.gemini, ~/.config/opencode (those that exist)
./install.sh --copy   # copy instead of symlink
```

Symlinks mean `git pull` updates every agent at once. The script skips any folder that already has a `daily-task-log` entry.

## Use it

Name the skill in your prompt:

- `use the daily-task-log skill for today`
- `daily-task-log: add yesterday, my work ran 11:35 AM to 12:49 PM IST`
- `daily-task-log: rebuild 08-10-2026 from git`

## Helper scripts

Both need only Python 3 and git, and the agent can run them for you.

```bash
python3 daily-task-log/scripts/git_timeline.py 2026-10-08          # commits in local time, grouped into slots
python3 daily-task-log/scripts/git_timeline.py 2026-10-08 --all    # include all branches
python3 daily-task-log/scripts/new_day.py 09-10-2026               # scaffold the day folder from templates
```

`git_timeline.py` is read-only. `new_day.py` never overwrites an existing file.

## Make it default for a project

Add this line to the project's `AGENTS.md` (or `CLAUDE.md`) so every agent knows the skill exists:

> Daily log: when asked to log or summarise a day's work, use the `daily-task-log` skill. Write to `daily-tasks/` and keep it out of git.

## Layout of this repo

```
daily-task-log/
  SKILL.md            the skill (name, description, steps, rules)
  templates/          slot, day and root readme templates
  scripts/            git_timeline.py, new_day.py
install.sh            install for all agents
```

MIT licensed.
