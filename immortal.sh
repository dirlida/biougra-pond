#!/bin/bash
# Immortal - watches daemon, restarts if dead. Does NOT mine itself.
cd ~/pond
while true; do
  if ! pgrep -f "pond_daemon.py" > /dev/null; then
    echo "[$(date -u +%FT%TZ)] immortal: daemon dead, restarting" >> logs/pond.log
    nohup python pond_daemon.py >> logs/pond.log 2>&1 &
  fi
  sleep 30
done
