#!/bin/bash
while true; do
  clear
  date -u
  python3 ~/biougra-pond/verify_chain.py
  echo "---"
  echo "chain len: $(python3 -c 'import json; print(len(json.load(open("chain.json"))))')"
  echo "LAST.txt: $(cat LAST.txt)"
  echo "--- log tail ---"
  tail -n 5 logs/daemon.log
  if [ "$(cat LAST.txt)" -ge 10 ]; then
    echo "✅ Pushed block 10!"
    break
  fi
  sleep 60
done
