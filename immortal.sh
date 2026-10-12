#!/data/data/com.termux/files/usr/bin/sh
# immortal v2.1 - Biougra Pond - with notification + self-heal
termux-wake-lock
while true; do
  # notification to stay foreground
  termux-notification --id biougra-pond --title "Biougra Pond ⛏️ #$(cat chain.json | python3 -c 'import json;print(len(json.load(open("chain.json"))))' 2>/dev/null)" --content "enforcer 10min | $(date)" --ongoing 2>/dev/null || true

  if ! pgrep -f pond_daemon.py > /dev/null; then
    echo "[$(date)] daemon dead - restarting" >> immortal.log
    nohup python3 pond_daemon.py >> daemon.log 2>&1 &
  fi

  # push every 5 blocks
  LEN=$(python3 -c "import json;print(len(json.load(open('chain.json'))))" 2>/dev/null)
  LAST_PUSH=$(cat PUSHED.txt 2>/dev/null || echo 0)
  if [ "$LEN" -ge $((LAST_PUSH+5)) ]; then
    bash push/check_push.sh 2>/dev/null || (git add chain.json; git commit -m "pond: block $LEN - 10min THE COUNT STABLE"; git push)
    echo $LEN > PUSHED.txt
  fi

  sleep 60
done
