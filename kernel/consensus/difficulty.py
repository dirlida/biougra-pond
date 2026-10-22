import json, pathlib
from datetime import datetime
ROOT=pathlib.Path.home()/"pond"
CHAIN=ROOT/"chain.json"
GENESIS_DIFF=2
ADJUST_EVERY=12
TARGET_BLOCK_TIME=600
MIN_DIFF=2
MAX_DIFF=3  # A13 CAP 3 - 000 is phone max
def parse_ts(v):
    if isinstance(v,int): return v
    try: return int(datetime.fromisoformat(v).timestamp())
    except: return 0
def get_difficulty(height=None):
    try:
        blocks=json.loads(CHAIN.read_text())
        if height is None: height=len(blocks)
        if height<5: return GENESIS_DIFF
        pow_blocks=[b for b in blocks if "nonce" in b][-ADJUST_EVERY:]
        if len(pow_blocks)<3: return GENESIS_DIFF
        times=[parse_ts(b.get("payload",b).get("ts",0)) for b in pow_blocks]
        times=[t for t in times if t>0]
        if len(times)<2: return GENESIS_DIFF
        elapsed=times[-1]-times[0]
        avg=elapsed/(len(times)-1)
        last_diff=pow_blocks[-1].get("difficulty",GENESIS_DIFF)
        if not isinstance(last_diff,int): last_diff=GENESIS_DIFF
        if avg < 400: new_diff=min(last_diff+1,MAX_DIFF)
        elif avg < 500: new_diff=last_diff
        elif avg > 900: new_diff=max(last_diff-1,MIN_DIFF)
        else: new_diff=last_diff
        print(f"[DIFF 10min A13 CAP3] h={height} avg={avg:.0f}s target=600s last={last_diff} -> {new_diff}")
        return new_diff
    except Exception as e:
        print(f"diff err {e}")
        return GENESIS_DIFF
if __name__=="__main__": print(f"difficulty={get_difficulty()}")
