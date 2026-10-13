#!/usr/bin/env python3
import os, json, time, glob
from datetime import datetime

POND = "."
blocks = sorted(glob.glob("block_*.json")) + sorted(glob.glob("*.block"))

print(f"=== BIOUGRA POND HEALTH — {datetime.now().strftime('%H:%M %d-%m-%Y')} ===\n")

# 1. Count
try:
    import subprocess
    res = subprocess.run(["python3", "verify.py"], capture_output=True, text=True, timeout=15)
    print(f"[verify.py]\n{res.stdout.strip()}\n{res.stderr.strip()}\n")
except Exception as e:
    print(f"[verify.py] FAILED: {e}\n")

# 2. Block timestamps - 10min rule check
files = sorted([f for f in os.listdir(POND) if f.startswith("block_")])
print(f"[BLOCKS] found {len(files)} files")
if files:
    times = []
    for f in files[-20:]: # last 20
        mt = os.path.getmtime(os.path.join(POND, f))
        times.append((f, mt))

    print("Last 20 blocks:")
    for f, mt in times:
        print(f" {f} — {datetime.fromtimestamp(mt).strftime('%H:%M:%S')}")

    # check 10min violations from block 36
    violations = 0
    for i in range(1, len(times)):
        diff = times[i][1] - times[i-1][1]
        if diff < 590: # less than ~9:50
            print(f" ⚠️ GAP VIOLATION: {times[i-1][0]} -> {times[i][0]} = {diff:.1f}s")
            violations += 1
    if violations == 0:
        print(" ✅ 10min rule OK on last 20\n")
    else:
        print(f" ❌ {violations} violations\n")

# 3. Disk / size health
total_size = sum(os.path.getsize(os.path.join(POND, f)) for f in files) if files else 0
print(f"[STORAGE] total blocks size: {total_size/1024:.1f} KB")
print(f"[PWD] {os.getcwd()}")

# 4. Git status for push readiness
try:
    res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, timeout=5)
    if res.stdout.strip():
        print(f"\n[GIT] Uncommitted:\n{res.stdout}")
    else:
        print("\n[GIT] ✅ Clean to push")

    res = subprocess.run(["git", "log", "--oneline", "-5"], capture_output=True, text=True, timeout=5)
    print(f"[GIT] Last 5 commits:\n{res.stdout}")
except:
    print("\n[GIT] not a git repo or git not found")

print("\n=== END HEALTH ===")
