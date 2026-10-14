#!/bin/bash
echo "=== BIOUGRA PHONE STATUS ==="
echo "Time: $(date)"
echo ""
echo "-- BATTERY --"
termux-battery-status 2>/dev/null || echo "install: pkg install termux-api"
echo ""
echo "-- CPU / LOAD --"
uptime
echo ""
cat /proc/loadavg 2>/dev/null && echo "loadavg (1/5/15 min)"
echo ""
echo "-- RAM --"
free -h 2>/dev/null || cat /proc/meminfo | head -20
echo ""
echo "-- STORAGE --"
df -h | grep -E "data|storage|/"
echo ""
echo "-- TEMP --"
cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null | awk '{print $1/1000 "°C"}' | head -5
echo ""
echo "-- PROCESSES (top) --"
ps -o pid,%cpu,%mem,cmd --sort=-%cpu | head -15
echo ""
echo "-- BIOUGRA --"
python3 verify.py
cat immortal.log | tail -5
echo ""
echo "Phone unbothered? YES"
