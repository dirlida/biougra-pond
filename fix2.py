import json
data=open('chain.json','r').read()
print(len(data))
# 805023 is where extra starts, so valid json is 0:805023
valid=data[:805023].rstrip().rstrip(',')
# ensure ends with ]
if not valid.endswith(']'):
    valid=valid+']'
arr=json.loads(valid)
print("loaded",len(arr))

thesis={"idx":1453,"type":"thesis","subtype":"resultful_thesis_v1","timestamp_utc":"2026-10-23T17:14:00Z","timestamp_ma":"2026-10-23T18:14:00+01:00","anchor_hash":"00012fa8f9462bb873ea87fe446316e28ab83e76e84509b1da601f851f07966b","baseline":{"height":1417,"idx":1416,"sha":"0c0c72b7"},"ghoul":{"version":"V5.4","pid":2877,"validators":"ZERO"},"motto":"Attachment = Latency. Latency = Fall velocity.","location":"Biougra, MA","thesis":"A Nokia burner can outlive your ass. A rock outlives AI. Longevity is not victory. Counting Matters = AI wins. Universal Matters = Humans judged."}
arr.append(thesis)
open('chain.json','w').write(json.dumps(arr))
print("fixed new len",len(arr))
