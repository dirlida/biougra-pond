#!/data/data/com.termux/files/usr/bin/bash
echo "=== TREE kernel ==="
find kernel -type f | sort
echo
echo "=== TREE attic ==="
find attic -type f | sort
echo
echo "=== CHAIN WRITERS ==="
grep -R "chain.json\|save_chain\|atomic_write" --include="*.py" --include="*.sh" -n kernel pond.py attic 2>&1 | head -n 150
echo
echo "=== CRONTAB ==="
crontab -l 2>&1
cat attic/cron.txt 2>&1
echo
echo "=== OTS GUARD ==="
cat attic/ots_guard.sh
echo
echo "=== FORK_GUARD ==="
ls -l kernel/consensus/fork_guard.py kernel/consensus/health.py pond.py attic/scripts/pond_daemon.py 2>&1
echo "--- fork_guard.py ---"
cat kernel/consensus/fork_guard.py
echo "--- pond.py head ---"
head -n 150 pond.py
echo
echo "=== LOCKS ==="
ls -lR attic/*.lock attic/**/*.lock 2>&1
ls -l *.lock */*.lock 2>&1
echo
echo "=== STATE PATHS ==="
ls -l chain.json kernel/state/chain.json embassy/public/chain.json 2>&1
realpath chain.json kernel/state/chain.json embassy/public/chain.json 2>&1 || readlink -f chain.json; readlink -f kernel/state/chain.json; readlink -f embassy/public/chain.json
echo
echo "=== HEALTH ==="
cat kernel/consensus/health.py
