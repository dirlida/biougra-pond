#!/bin/bash
cd /data/data/com.termux/files/home/pond
termux-wake-lock
echo "[IMMORTAL v2] started $(date -u)"
while true; do
  termux-wake-lock
  git pull origin main --quiet 2>/dev/null || true
  if [ -f .kernel_updated ]; then
    pkill -9 -f pond_daemon.py || true
    rm .kernel_updated
    sleep 2
  fi
  if ! pgrep -f pond_daemon.py > /dev/null; then
    echo "[IMMORTAL] resurrect $(date -u) height $(cat LAST.txt)"
    pkill -9 -f pond_daemon.py || true
    sleep 1
    nohup python3 pond_daemon.py > nohup.out 2>&1 &
  else
    echo "[IMMORTAL] alive $(date -u) height $(cat LAST.txt) count $(cat chain.json | grep -c hash)"
  fi
  sleep 60
done
