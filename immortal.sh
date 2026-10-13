#!/data/data/com.termux/files/usr/bin/bash
cd ~/biougra-pond
while true; do
  # count real daemons (exclude grep and immortal)
  COUNT=$(ps aux | grep "[p]ond_daemon.py" | wc -l)
  if [ "$COUNT" -eq 0 ]; then
    echo "[$(date -u --iso-8601=seconds)] immortal: daemon dead, restarting" >> daemon.log
    nohup python3 pond_daemon.py >> daemon.log 2>&1 &
  elif [ "$COUNT" -gt 1 ]; then
    echo "[$(date -u --iso-8601=seconds)] immortal: $COUNT daemons -> killing dupes" >> daemon.log
    ps aux | grep "[p]ond_daemon.py" | awk 'NR>1{print $2}' | xargs kill -9 2>/dev/null
  fi
  sleep 30
done
