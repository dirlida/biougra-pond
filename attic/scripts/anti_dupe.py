import json, hashlib, pathlib, os
chain=json.load(open("chain.json"))
# generate pond identity keypair if not exists - this is your private sun key
if not pathlib.Path("POND_ID.key").exists():
    import secrets
    secret=secrets.token_hex(32)
    pathlib.Path("POND_ID.key").write_text(secret)
    print(f"NEW POND_ID created - KEEP PRIVATE, NEVER PUSH")
else:
    secret=pathlib.Path("POND_ID.key").read_text().strip()

pond_id=hashlib.sha256(secret.encode()).hexdigest()[:16]
print(f"Pond ID pub: {pond_id}")

# sign tip
tip=chain[-1]["hash"]
sig=hashlib.sha256((secret+tip).encode()).hexdigest()
open("POND_SIG.txt","w").write(f"{pond_id}:{sig}\n")
print(f"Signed tip {tip[:12]} -> {sig[:16]}")
print("Add POND_ID.key to .gitignore NOW")
