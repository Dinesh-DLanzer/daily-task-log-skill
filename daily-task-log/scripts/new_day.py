#!/usr/bin/env python3
"""Scaffold a day folder in daily-tasks/ from the templates (never overwrites).

Usage: new_day.py [DD-MM-YYYY] [--root daily-tasks]

Creates <root>/readme.md (if missing) and <root>/<date>/readme.md (if missing).
Slot files are written by the agent once the times are known.
"""
import argparse
import datetime as dt
import pathlib

T = pathlib.Path(__file__).resolve().parent.parent / "templates"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("day", nargs="?", help="DD-MM-YYYY (default: today, local)")
    p.add_argument("--root", default="daily-tasks")
    a = p.parse_args()
    d = dt.datetime.strptime(a.day, "%d-%m-%Y") if a.day else dt.datetime.now()
    name = d.strftime("%d-%m-%Y")
    root = pathlib.Path(a.root)
    (root / name).mkdir(parents=True, exist_ok=True)
    for dest, tpl in ((root / "readme.md", "root-readme.md"), (root / name / "readme.md", "day-readme.md")):
        if dest.exists():
            print("exists  ", dest)
        else:
            dest.write_text(
                (T / tpl).read_text().replace("DD-MM-YYYY", name).replace("(Day)", f"({d:%a})")
            )
            print("created ", dest)


if __name__ == "__main__":
    main()
