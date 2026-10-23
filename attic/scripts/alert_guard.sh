#!/bin/bash
# If PAUSED file exists, skip alerts
if [ -f ~/pond/PAUSED ] || [ -f ~/pond/PRUNED ]; then
  exit 0
fi
# else run your usual alert script
python ~/pond/send_alert.py
