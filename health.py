import subprocess, json
from datetime import datetime, timezone
r=subprocess.run(["python","verify.py"], capture_output=True, text=True)
print(r.stdout)
if r.returncode!=0:
    print(f"--- POND HEALTH ---\nstatus: 🔴 VERIFY FAIL\n{r.stderr}")
    exit(1)
c=json.load(open("chain.json"))
def pdt(s): return datetime.fromisoformat(s.replace("Z","+00:00"))
last_ts=pdt(c[-1]["payload"]["ts"])
age=(datetime.now(timezone.utc)-last_ts).total_seconds()/60
print("--- POND HEALTH ---")
print(f"blocks: {len(c)}\nlast: {c[-1]['hash'][:12]} age: {age:.1f}m ago")
print(f"size: {len(json.dumps(c))/1024:.1f}KB")
print(f"status: {'🟢 LIVE' if age<12 else '🟡 LATE'}")
