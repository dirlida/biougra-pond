#!/usr/bin/env python3
"""Manual one-shot miner - uses kernel lock, cannot collide with daemon"""
from kernel import mine_and_save, auto_push, log, safe_load_chain
from datetime import datetime, timezone, timedelta

chain = safe_load_chain()
last_ts = datetime.fromisoformat(chain[-1]['payload']['ts'].replace("Z","+00:00"))
now = datetime.now(timezone.utc)
diff = (now - last_ts).total_seconds()

if diff < 600:
    log(f"hammer: last block {len(chain)-1} only {diff:.0f}s ago, mining anyway (manual override)")
    
block = mine_and_save()
log(f"Mined {block['index']} | {block['hash'][:12]}")
auto_push(block['index'])
