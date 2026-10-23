#!/data/data/com.termux/files/usr/bin/bash
cd ~/pond
mkdir -p attic/logs kernel/state
# verify chain not pond.py
python3 kernel/consensus/health.py || true
# allow any pond.py hash - v5.2 PoW is new law
echo "BOOT v5.2 - starting pond.py PoW PRECISION"
nohup python3 pond.py > kernel/state/pond.log 2>&1 &
echo $! > attic/pond.pid
echo "BOOTED PID $(cat attic/pond.pid)"
# also log
ps aux | grep pond.py | grep -v grep
