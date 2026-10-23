#!/data/data/com.termux/files/usr/bin/bash
set -e
cd ~/pond
PIDFILE=~/pond/.miner.pid

# ONE MINER ONLY - kill old if exists
if [ -f "$PIDFILE" ]; then
  old=$(cat $PIDFILE)
  if kill -0 $old 2>/dev/null; then
    echo "[$(date -u)] KILL old miner $old"
    kill -9 $old || true
  fi
  rm -f $PIDFILE .pond.lock
fi
echo $$ > $PIDFILE
echo "[$(date -u)] START single miner $$ - Biougra embassy"

# absolute counting truth log
LOG=~/pond/embassy_truth.log
echo "=== SESSION $(date -u) PID $$ ===" >> $LOG

count=0
while true; do
  count=$((count+1))
  rm -f .pond.lock
  echo "[$(date -u)] ATTEMPT #$count mine" | tee -a $LOG pond.log
  out=$(python -c "import sys; sys.path.insert(0, "attic/scripts"); import pond; r=pond.mine_and_save(); print(r)" 2>&1)
  echo "$out" | tee -a pond.log $LOG
  
  if echo "$out" | grep -q "MINED"; then
    bnum=$(echo "$out" | grep -o "MINED [0-9]*" | awk '{print $2}')
    echo "[$(date -u)] SUCCESS MINED $bnum" >> $LOG
    git add chain.json 2>&1 | tee -a $LOG
    git commit -m "$bnum btc $(python -c 'import json; print(json.load(open("chain.json"))[-1].get("btc_height",0))') truth" 2>&1 | tee -a $LOG
    git push origin main 2>&1 | tee -a $LOG
  fi
  
  if echo "$out" | grep -q "TOO FAST"; then
    diff=$(echo "$out" | grep -o "TOO FAST [0-9.]*" | awk '{print $3}' | cut -d. -f1)
    wait=$((615 - diff + 10))
    if [ $wait -lt 0 ]; then wait=10; fi
    echo "[$(date -u)] TOO FAST ${diff}s -> wait ${wait}s outside lock" | tee -a $LOG pond.log
    sleep $wait
  else
    python health.py 2>&1 | tee -a pond.log $LOG
    echo "[$(date -u)] SLEEP 615" | tee -a $LOG pond.log
    sleep 615
  fi
done
