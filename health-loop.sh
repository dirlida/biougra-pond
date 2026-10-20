#!/bin/bash
while true; do
  cd ~/pond && python3 health.py >> health.log 2>&1
  sleep 1800
done
