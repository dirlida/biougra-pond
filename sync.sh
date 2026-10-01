#!/data/data/com.termux/files/usr/bin/bash
set -e
eval $(ssh-agent -s) >/dev/null
ssh-add ~/.ssh/pond 2>/dev/null || ssh-add ~/.ssh/id_ed25519 2>/dev/null || true
cd ~/biougra-pond
git pull --rebase origin main || true
# merge pending if exists
if [ -f ~/storage/downloads/pond-pending.json ]; then
  echo "found pending from Downloads"
  cp ~/storage/downloads/pond-pending.json ./pending.json
fi
if [ -f ./pending.json ]; then
  python3 <<'PY'
import json, os, glob
chain=json.load(open('chain.json')) if os.path.exists('chain.json') else []
pending=json.load(open('pending.json')) if os.path.exists('pending.json') else []
# pending can be list or single
if isinstance(pending, dict): pending=[pending]
ids=set(b.get('id') for b in chain)
for b in pending:
  if b.get('id') not in ids:
    chain.append(b)
chain=sorted(chain, key=lambda x: x.get('id',0))
json.dump(chain, open('chain.json','w'), indent=2)
print(f"merged {len(pending)} -> total {len(chain)}")
PY
  rm -f pending.json
  rm -f ~/storage/downloads/pond-pending.json
fi
git add chain.json
git commit -m "pond sync $(date -Iseconds) [$(hostname)]" || echo "nothing to commit"
git push origin main
echo "✅ PUSHED forever via SSH"
git log --oneline -3
