
import pathlib, hashlib, os
ROOT=pathlib.Path.home()/"pond"/"keys"
PIN=os.environ.get("POND_PIN","biougra-a13-pond-embassy").encode()
def xor_encrypt(data: bytes) -> bytes:
    key=hashlib.sha256(PIN).digest()
    return bytes(b ^ key[i%len(key)] for i,b in enumerate(data))
def encrypt_keys():
    for name in ["cold.key","hot.key","stamp.key"]:
        p=ROOT/name
        if not p.exists(): continue
        if (ROOT/f"{name}.enc").exists(): continue
        data=p.read_bytes()
        if len(data)>200: continue
        enc=xor_encrypt(data)
        (ROOT/f"{name}.enc").write_bytes(enc)
        print(f"[KEYS] encrypted {name}")
if __name__=="__main__":
    encrypt_keys()
