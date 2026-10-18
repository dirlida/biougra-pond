#!/bin/sh
cd ~/pond
nohup python3 auto_last.py > auto_last.log 2>&1 &
echo "auto_last started $(date) pid $!"
