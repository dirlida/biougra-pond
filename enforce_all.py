import pathlib, subprocess, textwrap, os

# 1. verify.py - FULL KERNEL LAW ENFORCEMENT
verify_code = '''# KERNEL LAW v1 ENFORCEMENT
# Block 1eeff99 onward - hammered
import json, sys
from datetime import datetime, timezone

CANONICAL_FILE = "chain.json"
APPROVAL_THRESHOLD = 615
TIME_RULE_START = 36

def parse_utc_z(ts: str):
    if not ts.endswith("Z"):
        raise ValueError(f"ts must be UTC Z, got: {ts}")
    try:
        if "." in ts:
            dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
        return dt.replace(tzinfo=timezone.utc)
    except Exception as e:
        raise ValueError(f"Invalid canonical time format: {ts} - {e}")

def verify():
    try:
        data = json.load(open(CANONICAL_FILE))
    except Exception as e:
        print(f"FAIL: cannot read {CANONICAL_FILE}: {e}")
        sys.exit(1)
    if not data:
        print("OK: empty chain")
        return
    for i in range(1, len(data)):
        prev = data[i-1]
        cur = data[i]
        try:
            prev_t = parse_utc_z(prev["ts"])
            cur_t = parse_utc_z(cur["ts"])
        except Exception as e:
            print(f"FAIL at block {cur.get('index', i)}: {e}")
            sys.exit(1)
        if cur.get("index", i) >= TIME_RULE_START:
            diff = (cur_t - prev_t).total_seconds()
            if diff < APPROVAL_THRESHOLD:
                print(f"FAIL at block {cur.get('index', i)}: REFUSED - only {diff}s since last, need {APPROVAL_THRESHOLD}s - KERNEL LAW RULE 4")
                sys.exit(1)
        if "prev_hash" in cur and "hash" in prev:
            if cur["prev_hash"]!= prev["hash"]:
                print(f"FAIL at block {i}: prev_hash mismatch")
                sys.exit(1)
    print(f"OK: {len(data)} blocks - KERNEL LAW v1 verified - 615 hammer active")

if __name__ == "__main__":
    verify()
'''

# 2. immortal.sh - CODE DOWN ONLY
immortal_code = '''#!/bin/bash
# KERNEL LAW v1 - RULE 2 - CODE DOWN ONLY
while true; do
  echo "[IMMORTAL] pulling kernel code..."
  git pull origin main --quiet
  if [ -f.kernel_updated ]; then
    echo "[IMMORTAL] kernel update detected, restarting..."
    pkill -f pond_daemon.py
    rm.kernel_updated
  fi
  if! pgrep -f pond_daemon.py > /dev/null; then
    echo "[IMMORTAL] starting pond_daemon.py"
    nohup python pond_daemon.py > pond.log 2>&1 &
  fi
  python verify.py || echo "[IMMORTAL] VERIFY FAIL - check chain"
  sleep 60
done
'''

# 3. pond_daemon.py - inject kernel_stamp if file exists
pond_path = pathlib.Path("pond_daemon.py")
if pond_path.exists():
    content = pond_path.read_text()
    if "def kernel_stamp" not in content:
        patch = '''
# KERNEL LAW v1 - RULE 4 ENFORCEMENT
from datetime import timezone
def kernel_stamp():
    now_utc = datetime.now(timezone.utc)
    ts_z = now_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    local_tag = now_utc.astimezone().isoformat()
    return ts_z, local_tag
'''
        # add import if missing
        if "from datetime import datetime" in content and "timezone" not in content:
            content = content.replace("from datetime import datetime", "from datetime import datetime, timezone")
        content = patch + "\\n" + content
        # replace old ts creation hint
        content = content.replace('datetime.utcnow().isoformat()', 'kernel_stamp()[0]')
        pond_path.write_text(content)
        print("✅ pond_daemon.py patched with kernel_stamp()")
    else:
        print("✅ pond_daemon.py already has kernel_stamp")
else:
    # create minimal if missing
    pond_path.write_text('''from datetime import datetime, timezone
def kernel_stamp():
    now_utc = datetime.now(timezone.utc)
    ts_z = now_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    local_tag = now_utc.astimezone().isoformat()
    return ts_z, local_tag
''')
    print("✅ pond_daemon.py created")

# write files
pathlib.Path("verify.py").write_text(verify_code)
print("✅ verify.py written - 615 hammer enforced")

pathlib.Path("immortal.sh").write_text(immortal_code)
os.chmod("immortal.sh", 0o755)
print("✅ immortal.sh written - CODE DOWN ONLY")

# smooth push
cmds = [
    ["git", "add", "verify.py", "immortal.sh", "pond_daemon.py"],
    ["git", "commit", "-m", "LAW ENFORCEMENT: KERNEL LAW v1 code - 615 hammer enforced - Rules 2,3,4 active in code"],
    ["git", "push", "origin", "main"]
]
for c in cmds:
    print(f"$ {' '.join(c)}")
    subprocess.run(c, check=False)

print("✅ ALL LAWS ENFORCED - hammered in CODE")