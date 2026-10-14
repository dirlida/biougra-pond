import json, os, subprocess, datetime
from pathlib import Path

print(f"=== BIOUGRA POND KERNEL HEALTH — {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} ===")
print()

# 1. KERNEL LAW paper exists?
print("[LAW] KERNEL_LAW.md:", "OK" if Path("KERNEL_LAW.md").exists() else "MISSING!")
if Path("KERNEL_LAW.md").exists():
    print(f"      size: {Path('KERNEL_LAW.md').stat().st_size} bytes")

# 2. verify.py hammer
print("\n[verify.py]")
os.system("python verify.py")

# 3. chain THE COUNT
print()
try:
    chain = json.loads(Path("chain.json").read_text())
    print(f"[CHAIN] {len(chain)} blocks - {Path('chain.json').stat().st_size/1024:.1f} KB")
    last = chain[-1]
    ts = last.get("payload", {}).get("ts", "no ts")
    print(f"[LAST] ts={ts} hash={last.get('hash','')[:16]}...")
    # check kernel law time rule
    if len(chain) >= 2:
        from datetime import datetime, timezone
        def parse(s):
            return datetime.fromisoformat(s.replace("Z","+00:00"))
        prev_ts = chain[-2].get("payload",{}).get("ts")
        cur_ts = ts
        if prev_ts and cur_ts:
            diff = (parse(cur_ts) - parse(prev_ts)).total_seconds()
            print(f"[DIFF] {diff:.1f}s since prev - need 615s - {'OK' if diff>=615 or len(chain)<36 else 'FAIL'}")
except Exception as e:
    print(f"[CHAIN] error: {e}")

# 4. daemon alive?
print()
try:
    out = subprocess.check_output(["pgrep","-f","pond_daemon.py"], text=True)
    print(f"[DAEMON] RUNNING pid={out.strip()}")
except:
    print(f"[DAEMON] NOT RUNNING - immortal.sh should start it")

# 5. immortal alive?
try:
    out = subprocess.check_output(["pgrep","-f","immortal.sh"], text=True)
    print(f"[IMMORTAL] RUNNING pid={out.strip()}")
except:
    print(f"[IMMORTAL] NOT RUNNING - run: nohup bash immortal.sh &")

print(f"\n[PWD] {os.getcwd()}")
print("\n[GIT] Last 3:")
os.system("git log --oneline -3")
print("\n[GIT] Status:")
os.system("git status --porcelain")
print("\n=== END HEALTH ===")