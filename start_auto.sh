#!/bin/sh
cd ~/pond
rm -f .pond.lock .pond.lock.lock .ots_tmp_*
pkill -f pond_daemon
nohup python3 pond_daemon.py > pond.log 2>&1 &
echo "pond_daemon started $(date) pid $!"
