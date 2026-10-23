import json, pathlib, time, re
ROOT=pathlib.Path.home()/"pond"
CHAIN=ROOT/"chain.json"
QUEUE=ROOT/"kernel"/"modules"/"stamp"/"queue.json"
try:
    data=CHAIN.read_bytes()[-4096:]
    m_index=re.findall(b'"index":\s*(\d+)', data)
    m_hash=re.findall(b'"hash":\s*"([a-f0-9]+)"', data)
    idx=int(m_index[-1]) if m_index else 0
    h=m_hash[-1].decode() if m_hash else "0"*64
    q={"latest_index":idx,"latest_hash":h,"queued_at":int(time.time()),"ready_for_push":True,"note":"v5.2 PoW 00 block, wifi pending"}
    QUEUE.write_text(json.dumps(q, indent=2))
    print(f"queued #{idx} {h[:8]} ready")
except Exception as e:
    print(f"queue err {e}")
