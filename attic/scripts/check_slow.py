import json, datetime

with open('chain.json') as f:
    chain=json.load(f)

def get_ts(block):
    p=block.get('payload') or block
    return p.get('ts') or block.get('ts')

for num in [1033,1034,1035,1036,1037,1038]:
    if num >= len(chain):
        print(f"#{num} OUT OF RANGE len={len(chain)}")
        continue
    b=chain[num]
    ts=get_ts(b)
    try:
        dt=datetime.datetime.fromisoformat(str(ts).replace('Z','+00:00'))
    except:
        dt=ts
    prev_ts=get_ts(chain[num-1]) if num>0 else None
    gap=""
    if prev_ts and ts:
        try:
            t1=datetime.datetime.fromisoformat(str(ts).replace('Z','+00:00'))
            t0=datetime.datetime.fromisoformat(str(prev_ts).replace('Z','+00:00'))
            gap=f" gap={(t1-t0).total_seconds():.0f}s"
        except:
            pass
    h=b.get('hash','')[:12]
    print(f"#{num}: {dt} gap={gap} hash={h}")
print(f"TOTAL {len(chain)}")
