#!/usr/bin/env bash
# Install the daily-task-log skill for every coding agent found on this machine.
# Usage: ./install.sh [--copy]    (default: symlink, so `git pull` updates all agents)
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)/daily-task-log"
MODE="symlink"; [ "${1:-}" = "--copy" ] && MODE="copy"
CANON="$HOME/.agents/skills"   # shared location used by several agents

link() { # link <skills dir>
  local dir="$1" dest="$1/daily-task-log"
  mkdir -p "$dir"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    [ "$(readlink "$dest" 2>/dev/null)" = "$SRC" ] && { echo "ok       $dest"; return; }
    echo "skipped  $dest (already exists; remove it first to replace)"; return
  fi
  if [ "$MODE" = copy ]; then cp -R "$SRC" "$dest"; else ln -s "$SRC" "$dest"; fi
  echo "$MODE  $dest"
}

link "$CANON"
[ -d "$HOME/.claude" ]          && link "$HOME/.claude/skills"
[ -d "$HOME/.codex" ]           && link "$HOME/.codex/skills"
[ -d "$HOME/.gemini" ]          && link "$HOME/.gemini/skills"
[ -d "$HOME/.config/opencode" ] && link "$HOME/.config/opencode/skills"
echo
echo "Done. In a prompt, say: use the daily-task-log skill"
