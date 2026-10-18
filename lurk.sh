#!/bin/sh
while true; do
clear
LAST_TS=$(python3 -c "import json; c=json.load(open('chain.json')); print(c[-1]['payload']['ts'])")
LAST_SEC=$(python3 -c "from datetime import datetime,timezone; import json; c=json.load(open('chain.json')); t=datetime.fromisoformat(c[-1]['payload']['ts'].replace('Z','+00:00')); print(int(t.timestamp()))")
NOW_SEC=$(date +%s)
DIFF=$((NOW_SEC - LAST_SEC))
TIP=$(cat LAST.txt | cut -c1-12)
COUNT=$(python3 -c "import json; print(len(json.load(open('chain.json'))))")
LAST_IDX=$(python3 -c "import json; print(json.load(open('chain.json'))[-1]['index'])")

echo "=== POND $LAST_IDX LURK - $TIP - $COUNT blocks ==="
echo "Last: $LAST_TS ( $DIFF sec ago )"
echo "Tip $TIP Blocks $COUNT"
if [ $DIFF -lt 590 ]; then
  echo "⏳ WAIT $((590-DIFF))s until 590s window"
elif [ $DIFF -le 900 ]; then
  echo "🟢 MINE NOW! $DIFF sec in window"
else
  echo "🔴 LATE $DIFF sec >900 - mine ASAP"
fi
echo ""
python3 verify.py
echo ""
echo "Last 3:"
python3 -c "import json; c=json.load(open('chain.json')); [print(f\"{b['index']} {b['hash'][:12]} {b['payload']['ts'][11:19]} sun={b['payload'].get('sunAltitude','-')} btc={b['payload'].get('btcHeight','-')}\") for b in c[-3:]]"
sleep 5
done
