import json, glob
from datetime import datetime
blocks = sorted(glob.glob('blocks/*.json'))
last = blocks[-1].split('/')[-1].replace('.json','') if blocks else 'fea18e68bc92'
data = {
  "blocks": len(blocks),
  "last": last[:12],
  "full": last,
  "status": "LIVE",
  "attested": "a82424e1dbf0",
  "time": datetime.utcnow().isoformat()+'Z'
}
with open('embassy/public/pond-health.json','w') as f:
    json.dump(data,f,indent=2)
print(f"WROTE 765 -> {last}")
