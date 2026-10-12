#!/bin/bash
while true; do
  if ! pgrep -f "pond_daemon.py" > /dev/null; then
    echo "$(date) - daemon dead, restarting" >> immortal.log
    nohup python3 ~/biougra-pond/pond_daemon.py >> ~/biougra-pond/daemon.log 2>&1 &
  fi
  sleep 60
done
