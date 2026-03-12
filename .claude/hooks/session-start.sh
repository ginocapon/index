#!/bin/bash
set -euo pipefail

# Esegui solo in ambiente remoto (Claude Code on the web)
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Installa dipendenze Node.js se presente package.json
if [ -f "$CLAUDE_PROJECT_DIR/package.json" ]; then
  cd "$CLAUDE_PROJECT_DIR"
  npm install
fi
