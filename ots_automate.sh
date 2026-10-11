#!/bin/bash
echo "Auto OTS upgrade poll — 10 blocks 1725faf5"
for i in {1..12}; do
  echo "--- try $i/12 $(date) ---"
  ots upgrade chain.json.ots
  ots upgrade chain_v1_9.json.ots
  v10=$(ots verify chain.json.ots 2>&1)
  v9=$(ots verify chain_v1_9.json.ots 2>&1)
  echo "$v10"
  if echo "$v10" | grep -q "Success"; then
    echo "✅ v10 ATTESTED"
    git add chain.json.ots chain_v1_9.json.ots
    git commit -m "OTS attested Bitcoin 10 blocks 1725faf5 $v10"
    git push
    bash RUNME.sh
    exit 0
  fi
  echo "pending, sleep 10 min..."
  sleep 600
done
echo "still pending after 2h — run again later"
