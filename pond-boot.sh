#!/data/data/com.termux/files/usr/bin/bash
# Biougra Pond v1.2 - SINGLE DAEMON ONLY - 22 blocks genesis

pkill -9 -f pond_daemon 2>/dev/null
pkill -9 -f pond_30q 2>/dev/null
rm -f ~/biougra-pond/ots.pid
sleep 1

termux-wake-lock

cd ~/biougra-pond

# check if already running
if pgrep -f pond_daemon > /dev/null; then
  echo "Pond already running"
  exit 0
fi

echo "[$(date)] boot: starting single daemon, chain 22 blocks" >> daemon.log
nohup python pond_daemon.py >> daemon.log 2>&1 &
echo "Pond booted PID $! - 10m block"
