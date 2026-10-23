import hashlib, pathlib, json, time
ROOT = pathlib.Path.home() / "pond"
INBOX = ROOT / "kernel" / "modules" / "stamp" / "inbox"
OUTBOX = ROOT / "kernel" / "modules" / "stamp" / "outbox"
INBOX.mkdir(parents=True, exist_ok=True)
OUTBOX.mkdir(parents=True, exist_ok=True)
def stamp_file(p):
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    out = {"file": str(p.name), "sha256": h, "ts": int(time.time())}
    (OUTBOX / f"{h[:12]}.json").write_text(json.dumps(out))
    return h
