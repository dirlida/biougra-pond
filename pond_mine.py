import json,hashlib,datetime
chain=json.load(open("chain.json"))
last=chain[-1]
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
seed=f"{last['hash']}{now}30.12613,-9.37437"
new_hash=hashlib.sha256(seed.encode()).hexdigest()
print(f"would mine {new_hash[:16]} len {len(chain)+1} - dry run OK")
