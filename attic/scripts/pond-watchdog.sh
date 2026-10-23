#!/bin/bash
CHAIN="$HOME/pond/chain.json"
LOG="$HOME/pond/watchdog.log"
MAX=1200
AGE=$(python3 -c "import json,datetime; c=json.load(open('$HOME/pond/chain.json'))[-1]; dt=datetime.datetime.fromisoformat(c['payload']['ts'].replace('Z','+00:00')); print(int((datetime.datetime.now(datetime.timezone.utc)-dt).total_seconds()))")
echo "$(date -u +%FT%TZ) age ${AGE}s" >> "$LOG"
if [ "$AGE" -gt "$MAX" ]; then
 pkill -9 -f pond_daemon.py
 sleep 2
 cd ~/pond && ./pond.sh start >> "$LOG" 2>&1
 echo "$(date -u +%FT%TZ) restarted" >> "$LOG"
fi
