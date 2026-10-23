import json, pathlib, time, datetime
ROOT = pathlib.Path.home() / "pond"
CLOCK = ROOT / "kernel/state/POND_CLOCK.json"
CHAIN = ROOT / "chain.json"

# Baseline auto-corrected to real UTC 11:27 2026-10-23
BASELINE = {
  "height": 1424,
  "index": 1423,
  "ts": "2026-10-23T11:27:00Z",
  "sha": "a0f0813b69dc",
  "git_commit": "5d8feba",
  "avg_block_sec": 600
}

def load_chain_last():
  try:
    data = json.loads(CHAIN.read_text())
    last = data[-1]
    return last['index'], last['payload']['ts']
  except:
    return BASELINE["index"], BASELINE["ts"]

def get_pond_time():
  try:
    curr_idx, curr_ts_str = load_chain_last()
    baseline_dt = datetime.datetime.fromisoformat(BASELINE["ts"].replace('Z','+00:00'))
    curr_dt = datetime.datetime.fromisoformat(curr_ts_str.replace('Z','+00:00'))
    blocks_since = curr_idx - BASELINE["index"]
    pond_elapsed_sec = blocks_since * BASELINE["avg_block_sec"]
    pond_now = baseline_dt + datetime.timedelta(seconds=pond_elapsed_sec)
    real_now = datetime.datetime.now(datetime.timezone.utc)
    drift_sec = (real_now - pond_now).total_seconds()
    return {
      "baseline": BASELINE,
      "current_index": curr_idx,
      "blocks_since_baseline": blocks_since,
      "pond_now_iso": pond_now.isoformat(),
      "real_now_iso": real_now.isoformat(),
      "pond_elapsed_sec": pond_elapsed_sec,
      "drift_sec": drift_sec,
      "drift_min": round(drift_sec/60,1),
      "is_cuckoo": abs(drift_sec) > 900,
      "status": "SYNCED" if abs(drift_sec) < 600 else "CUCKOO",
      "note": "POND clock uses block height as wall clock - survives LLM resets"
    }
  except Exception as e:
    return {"error": str(e), "baseline": BASELINE}

def save_clock():
  info = get_pond_time()
  CLOCK.write_text(json.dumps(info, indent=2))
  return info

if __name__ == "__main__":
  info = save_clock()
  print(json.dumps(info, indent=2))
