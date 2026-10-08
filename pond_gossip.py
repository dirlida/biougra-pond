import json, hashlib, hmac, os, time, base64
SECRET_SEED = "biougra-pond-4138350-genesis"
def load_wallet():
    with open("wallet.json","rb") as f:
        data=f.read()
        j=json.loads(data)
        return j, data
def sign_wallet(raw_bytes):
    sig_extra = b""
    if os.path.exists("bell_log.txt"):
        sig_extra = open("bell_log.txt","rb").read()[:1024]
    return hmac.new(SECRET_SEED.encode()+sig_extra, raw_bytes, hashlib.sha256).hexdigest()
def armor_check():
    w, raw = load_wallet()
    calc_hash = hashlib.sha256(raw).hexdigest()[:16]
    hmac_sig = sign_wallet(raw)
    S = w.get("proof",{}).get("S_measured",0)
    if S < 2.0:
        raise SystemExit("tamper detected: S < 2")
    return {"wallet_hash":calc_hash, "hmac":hmac_sig, "S":S, "valid":True}
def share_qr_payload():
    w, raw = load_wallet()
    a=armor_check()
    payload = {"w": w, "h": a["wallet_hash"], "mac": a["hmac"][:24], "ts": int(time.time())}
    b64 = base64.b64encode(json.dumps(payload).encode()).decode()
    print(b64)
    open("pond_share.txt","w").write(b64)
if __name__=="__main__":
    import sys
    if len(sys.argv)>1 and sys.argv[1]=="--share":
        share_qr_payload()
    else:
        print(armor_check())
