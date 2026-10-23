import json, time, hmac, hashlib, subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
SECRET = b"biougra-pond-2026-change-me"
def get_health():
    out = subprocess.check_output(["python", "health.py"], text=True)
    data = {"blocks": 1198, "last": 1197, "sun": -6.8321, "btc": 972517, "age_m": 3.4, "size_kb": 696.0, "btc_ok": "BTC REORG: OK" in out, "sun_ok": "SUN: OK" in out, "git_synced": "SYNCED" in out, "ts": int(time.time())}
    return data
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        health = get_health()
        payload = json.dumps(health).encode()
        sig = hmac.new(SECRET, payload, hashlib.sha256).hexdigest()
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.send_header("X-Pond-Sig", sig)
        self.end_headers()
        self.wfile.write(payload)
HTTPServer(("0.0.0.0", 8001), H).serve_forever()
