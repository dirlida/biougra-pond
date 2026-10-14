#!/bin/bash
# KERNEL LAW v1 - RULE 2 - CODE DOWN ONLY - FIXED
while true; do
  echo "[IMMORTAL] pulling kernel code..."
  git pull origin main --quiet
  if [ -f .kernel_updated ]; then
    echo "[IMMORTAL] kernel update detected, restarting..."
    pkill -f pond_daemon.py
    rm .kernel_updated
  fi
  if ! pgrep -f pond_daemon.py > /dev/null; then
    echo "[IMMORTAL] starting pond_daemon.py"
    nohup python pond_daemon.py > pond.log 2>&1 &
  fi
  python verify.py || echo "[IMMORTAL] VERIFY FAIL - check chain"
  sleep 60
done