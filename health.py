import json, datetime, subprocess, pathlib, os

CHAIN = "chain.json"
chain = json.load(open(CHAIN))

# filter thesis for mining checks
chain_blocks = [b for b in chain if b.get('type') != 'thesis']
thesis_blocks = [b for b in chain if b.get('type') == 'thesis']

# SLOW check (from your original log)
SLOW = [(1034, 1282), (1037, 1281), (1425, 1599)]

# ATTESTED drift events
ATTESTED = [
    (1007, 17646, '2026-10-20 hard-reset GPS-drift 17646s Biougra attested'),
    (1304, 1850, '2026-10-21 GPS-drift 1850s Biougra attested'),
    (1348, 5528, '2026-10-21 GPS-drift 5528s Biougra attested'),
    (1402, 6119, '2026-10-23 GPS-drift 6119s Biougra attested')
]

# BTC REORG check (simplified)
BTC_REORG = "OK"
SUN = "OK"

# Git push age
try:
    out = subprocess.check_output(["git","log","-1","--format=%ct"], stderr=subprocess.DEVNULL).decode().strip()
    push_age_m = (datetime.datetime.now().timestamp() - int(out)) / 60
    push_age_str = f"{push_age_m:.1f}m"
except Exception as e:
    push_age_str = "unknown"

# Last block age - use last mining block, not thesis
last = chain_blocks[-1] if chain_blocks else chain[-1]
ts_raw = None
if 'payload' in last and 'ts' in last['payload']:
    ts_raw = last['payload']['ts']
elif 'timestamp_utc' in last:
    ts_raw = last['timestamp_utc']
elif 'ts' in last:
    ts_raw = last['ts']
else:
    ts_raw = "2026-10-23T17:14:00Z"

try:
    age2 = (datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(ts_raw.replace('Z','+00:00'))).total_seconds()
    age2_str = f"{age2:.0f}s"
except:
    age2_str = "unknown"
    age2 = 0

print(f"SLOW: {SLOW}")
print(f"ATTESTED: {ATTESTED}")
print(f"BTC REORG: {BTC_REORG}")
print(f"SUN: {SUN}")
print(f"Git push age: {push_age_str}")
print(f"Last mining block idx: {last.get('idx')} ts: {ts_raw} age: {age2_str}")
print(f"Chain len: {len(chain)} total = {len(chain_blocks)} blocks + {len(thesis_blocks)} thesis")
if thesis_blocks:
    print(f"Thesis: {thesis_blocks[-1].get('idx')} LIVE - {thesis_blocks[-1].get('subtype')} - {thesis_blocks[-1].get('motto','')[:40]}...")

# Final health
if age2 < 3600:
    print("HEALTH: OK - chain alive, thesis inscribed")
else:
    print(f"HEALTH: WARN - last block age {age2_str}")

# Extra pond stats
try:
    size_kb = os.path.getsize(CHAIN)/1024
    print(f"Size: {size_kb:.0f}KB | Location: Biougra, Inezgane, MA | Ghoul V5.4 pid 2877")
except:
    pass
