#!/bin/zsh

set -euo pipefail

PROJECT_DIR="/Users/l.eatonnortheastern.edu/Documents/Music/video-to-mp3-studio"
APP_URL="http://127.0.0.1:5001"
LOG_DIR="$HOME/Library/Logs/VideoToMP3Studio"
LOG_FILE="$LOG_DIR/app.log"
PID_FILE="$HOME/Library/Application Support/VideoToMP3Studio/server.pid"

mkdir -p "$LOG_DIR"
mkdir -p "$(dirname "$PID_FILE")"

is_running() {
  lsof -i tcp:5001 >/dev/null 2>&1
}

start_server() {
  cd "$PROJECT_DIR"
  source .venv/bin/activate
  nohup python3 app.py >>"$LOG_FILE" 2>&1 &
  echo $! >"$PID_FILE"
}

if ! is_running; then
  start_server
  sleep 2
fi

open "$APP_URL"
