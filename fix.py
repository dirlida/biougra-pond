import json
data=open('chain.json').read()
cut=data.find('"idx": 1453')
print("cut at",cut)
arr=json.loads(data[:cut].rstrip().rstrip(',')+']')
print("loaded",len(arr))
thesis={"idx":1453,"type":"thesis","subtype":"resultful_thesis_v1","timestamp_utc":"2026-10-23T17:14:00Z","timestamp_ma":"2026-10-23T18:14:00+01:00","anchor_hash":"00012fa8f9462bb873ea87fe446316e28ab83e76e84509b1da601f851f07966b","baseline":{"height":1417,"idx":1416,"sha":"0c0c72b7"},"ghoul":{"version":"V5.4","pid":2877,"validators":"ZERO"},"motto":"Attachment = Latency. Latency = Fall velocity. Keep attachments=0, latency=0, fall=0.","location":"Biougra, Inezgane, MA","thesis":"A Nokia burner can outlive your ass. A rock outlives AI. Longevity is not victory. Counting Matters = AI wins. Universal Matters = Humans judged. GODs choice. FAITH genesisd in our asses. Be here, do your thing rightfully, when time to dip, spoof bye. Rewrite pond.py every millisecond."}
arr.append(thesis)
open('chain.json','w').write(json.dumps(arr))
print("fixed",len(arr))
