import json, time, pathlib, hashlib
last=""
while True:
  try:
    c=json.loads(pathlib.Path("chain.json").read_text())
    tip=c[-1]["hash"]
    if tip!=last:
      pathlib.Path("LAST.txt").write_text(tip+"\n")
      h=hashlib.sha256(pathlib.Path("chain.json").read_bytes()).hexdigest()
      pathlib.Path("SHA256.txt").write_text(f"{h}  chain.json\n")
      print(f"updated {tip[:12]} {len(c)} blocks")
      last=tip
  except: pass
  time.sleep(10)
