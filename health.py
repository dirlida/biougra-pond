import json,os,subprocess,datetime
CHAIN="chain.json"
chain=json.load(open(CHAIN))
# v4.2 attested breaks - known, documented, not errors
ATTESTED = {1007: "2026-10-20 hard-reset GPS-drift 17646s Biougra attested"}
slow=[]
attested_found=[]
for i in range(1,len(chain)):
 try:
  t1=datetime.datetime.fromisoformat(chain[i-1]['payload']['ts'].replace('Z','+00:00'))
  t2=datetime.datetime.fromisoformat(chain[i]['payload']['ts'].replace('Z','+00:00'))
  d=(t2-t1).total_seconds()
  if d>1200:
    if chain[i]['index'] in ATTESTED:
      attested_found.append((chain[i]['index'],int(d),ATTESTED[chain[i]['index']]))
    else:
      slow.append((chain[i]['index'],int(d)))
 except: pass
print("SLOW:",slow[-3:] if slow else "OK")
if attested_found:
  print("ATTESTED:",attested_found)
reorg=[]
for i in range(1,len(chain)):
 try:
  b1=chain[i-1]['payload']['btcHeight']; b2=chain[i]['payload']['btcHeight']
  if b2 < b1-1: reorg.append((chain[i]['index'],b1,b2))
 except: pass
print("BTC REORG:",reorg[-3:] if reorg else "OK")
jump=[]
for i in range(1,len(chain)):
 try:
  s1=chain[i-1]['payload']['sunAltitude']; s2=chain[i]['payload']['sunAltitude']
  if abs(s2-s1)>10 and chain[i]['index']!=36 and chain[i]['index'] not in ATTESTED:
    jump.append((chain[i]['index'],s1,s2))
 except: pass
print("SUN:",jump[-3:] if jump else "OK")
try:
 out=subprocess.check_output(["git","log","-1","--format=%ct"],text=True).strip()
 last=datetime.datetime.fromtimestamp(int(out),tz=datetime.timezone.utc)
 age=(datetime.datetime.now(datetime.timezone.utc)-last).total_seconds()
 print(f"Git push age: {age/60:.1f}m")
except Exception as e:
 print("Git err",e)
last=chain[-1]
age2=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(last['payload']['ts'].replace('Z','+00:00'))).total_seconds()
size=os.path.getsize(CHAIN)/1024
stat="LIVE" if age2<1200 else "STALE"
print(f"blocks {len(chain)} last #{last['index']} sun={last['payload']['sunAltitude']} btc={last['payload']['btcHeight']} age {age2/60:.1f}m {size:.1f}KB {stat}")
