#!/bin/sh
cd ~/pond
rm -f .pond.lock .pond.lock.lock .ots_tmp_* .miner.pid
pkill -f pond_daemon 2>/dev/null
pkill -f mine_auto 2>/dev/null
pkill -f ots_guard 2>/dev/null

# A13 KERNEL — sealed v1304 — correct paths
mkdir -p attic/ots attic/logs attic/frozen kernel/state

# OTS guard — always
nohup bash "$HOME/pond/attic/ots_guard.sh" >/dev/null 2>&1 &
echo "ots_guard started"

# pond daemon — correct attic path
PYTHONPATH="$HOME/pond/attic/scripts:$HOME/pond/kernel:$PYTHONPATH" nohup python3 "$HOME/pond/attic/scripts/pond_daemon.py" > "$HOME/pond/attic/logs/pond.log" 2>&1 &
echo "pond_daemon started pid $! $(date)"

# mine auto backup miner — also correct path
PYTHONPATH="$HOME/pond/attic/scripts:$PYTHONPATH" nohup bash "$HOME/pond/attic/scripts/mine_auto.sh" > "$HOME/pond/attic/logs/mine.log" 2>&1 &
echo "mine_auto started"

# health loop if exists
[ -f attic/scripts/health-loop.sh ] && nohup bash attic/scripts/health-loop.sh >/dev/null 2>&1 &

sleep 2
ps aux | grep -E "pond|mine|health|ots_guard" | grep -v grep
python kernel/consensus/health.py
