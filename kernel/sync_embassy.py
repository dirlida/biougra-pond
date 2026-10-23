#!/usr/bin/env python3
"""Single source of truth: chain.json SHA = verify"""
import hashlib, json, pathlib
root=pathlib.Path.home()/"pond"
data=(root/"chain.json").read_bytes()
sha=hashlib.sha256(data).hexdigest()
chain=json.loads(data.decode())
last=chain[-1]
idx=last["index"]
h=len(chain)
payload=last["payload"]

# kernel state
(root/"kernel/state/chain.json").write_bytes(data)
(root/"kernel/state/SHA256.txt").write_text(sha+"\n")
(root/"kernel/state/LAST.txt").write_text(sha+"\n")
(root/"SHA256.txt").write_text(sha+"\n")

# embassy public
pub=root/"embassy/public"
pub.mkdir(exist_ok=True, parents=True)
(pub/"chain.json").write_bytes(data)
(pub/"blocks.json").write_bytes(data)
base=pub/"api"
base.mkdir(exist_ok=True, parents=True)
(base/"height.json").write_text(json.dumps({"height": h, "last": idx, "index": idx}, indent=2))
(base/"last_hash.json").write_text(json.dumps({"hash": last["hash"], "height": idx, "index": idx}, indent=2))
(base/"verify.json").write_text(json.dumps({"verify": sha, "ok": True, "hash": sha, "index": idx, "last_hash": last["hash"]}, indent=2))
status={"height": h, "index": idx, "last_hash": last["hash"], "verify": sha, "blocks": h, "live": True, "sun": payload.get("sunAltitude"), "btc": payload.get("btcHeight"), "ts": payload.get("ts"), "sha": sha}
(base/"status.json").write_text(json.dumps(status, indent=2))
print(f"SYNCED {h} idx={idx} sha={sha[:12]}")
