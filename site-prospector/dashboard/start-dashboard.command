#!/bin/bash
# Site Prospector - starts the dashboard (macOS). Double-click to open.
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then
  python3 dashboard-server.py
else
  echo "Python 3 not found. Install it from https://www.python.org/downloads/ (or: brew install python3) and try again."
  read -p "Press Enter to close..."
fi
