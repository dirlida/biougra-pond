#!/data/data/com.termux/files/usr/bin/bash
cd ~/pond
echo "PANIC v5.0 - $(date -u)" | tee -a attic/FORK_ALERT.md
python3 kernel/consensus/health.py | tee -a attic/FORK_ALERT.md
python3 kernel/consensus/replay.py | tee -a attic/FORK_ALERT.md
# kill writers but keep lock file
pkill -f "pond.py" || true
echo "Writers killed - manual boot.sh required after fix"
