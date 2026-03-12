#!/bin/zsh

set -euo pipefail

PROJECT_DIR="/Users/l.eatonnortheastern.edu/Documents/Music/video-to-mp3-studio"
APP_SCRIPT="$PROJECT_DIR/app.py"
APP_URL="http://127.0.0.1:5001"
LOG_DIR="$HOME/Library/Logs/VideoToMP3Studio"
LOG_FILE="$LOG_DIR/app.log"
PID_FILE="$HOME/Library/Application Support/VideoToMP3Studio/server.pid"
PYTHON_BIN="/opt/homebrew/bin/python3"
PYTHON_SITE_PACKAGES="$PROJECT_DIR/.venv/lib/python3.14/site-packages"
DOWNLOADS_DIR="$HOME/Downloads/Video to MP3 Studio"
COOKIES_DIR="$HOME/Documents/Video to MP3 Studio"

mkdir -p "$LOG_DIR"
mkdir -p "$(dirname "$PID_FILE")"

is_running() {
  lsof -i tcp:5001 >/dev/null 2>&1
}

wait_for_server() {
  for _ in {1..20}; do
    if is_running; then
      return 0
    fi
    sleep 1
  done
  return 1
}

start_server() {
  cd "$PROJECT_DIR"
  PYTHONPATH="$PYTHON_SITE_PACKAGES" \
  VIDEO_TO_MP3_DOWNLOADS_DIR="$DOWNLOADS_DIR" \
  VIDEO_TO_MP3_COOKIES_DIR="$COOKIES_DIR" \
  nohup "$PYTHON_BIN" "$APP_SCRIPT" >>"$LOG_FILE" 2>&1 &
  echo $! >"$PID_FILE"
}

if ! is_running; then
  start_server
  wait_for_server || exit 1
fi

open "$APP_URL"
