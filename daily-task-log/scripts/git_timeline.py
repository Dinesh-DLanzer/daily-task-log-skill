#!/usr/bin/env python3
"""Print one day's git commits in local time, grouped into time-slot clusters.

Usage: git_timeline.py YYYY-MM-DD [--gap MINUTES] [--repo PATH] [--all]

Local time is the machine's zone. Commits more than --gap minutes apart start a new
cluster (default 90). --all includes every branch. Each cluster gets a suggested
slot file name such as 11-35-AM-to-12-20-PM.md. Read-only: it only runs `git log`.
"""
import argparse
import datetime as dt
import subprocess
import sys


def slot_name(start, end):
    def part(d):
        return d.strftime("%I-%M-%p")
    return f"{part(start)}-to-{part(end)}.md"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("day", help="YYYY-MM-DD (local date)")
    p.add_argument("--gap", type=int, default=90, help="minutes of silence that starts a new slot")
    p.add_argument("--repo", default=".")
    p.add_argument("--all", action="store_true", help="include all branches")
    a = p.parse_args()

    try:
        day = dt.datetime.strptime(a.day, "%Y-%m-%d").astimezone()
    except ValueError:
        sys.exit("day must be YYYY-MM-DD")
    start = day.replace(hour=0, minute=0, second=0)
    end = start + dt.timedelta(days=1)
    cmd = ["git", "-C", a.repo, "log", f"--since={start.isoformat()}", f"--until={end.isoformat()}",
           "--format=%at|%h|%an|%s", "--reverse"]
    if a.all:
        cmd.insert(4, "--all")
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(out.stderr.strip() or "git log failed")

    commits = []
    for line in out.stdout.splitlines():
        at, sha, author, subject = line.split("|", 3)
        commits.append((dt.datetime.fromtimestamp(int(at)).astimezone(), sha, author, subject))
    if not commits:
        print(f"No commits on {a.day} (zone {start.tzname()}).")
        return

    clusters = [[commits[0]]]
    for c in commits[1:]:
        if (c[0] - clusters[-1][-1][0]).total_seconds() > a.gap * 60:
            clusters.append([])
        clusters[-1].append(c)

    print(f"{a.day}  zone {start.tzname()}  {len(commits)} commits  {len(clusters)} clusters (gap {a.gap} min)\n")
    for cl in clusters:
        s, e = cl[0][0], cl[-1][0]
        print(f"## {s:%I:%M %p} - {e:%I:%M %p}   suggested file: {slot_name(s, e)}")
        for t, sha, author, subject in cl:
            print(f"  {t:%H:%M}  {sha}  {author:<14} {subject[:110]}")
        print()
    print("Note: commit time is when work was saved, not when it started. Widen a slot's start using session times.")


if __name__ == "__main__":
    main()
