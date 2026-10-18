#!/data/data/com.termux/files/usr/bin/bash
set -e
cd ~/pond
echo "[embassy] syncing..."
python3 << 'PY'
import json, pathlib
chain = json.loads(pathlib.Path("chain.json").read_text())
blocks = chain[-500:]
pathlib.Path("embassy/public/chain.json").write_text(json.dumps(chain, indent=2))
pathlib.Path("embassy/public/blocks.json").write_text(json.dumps(blocks, indent=2))
print(f"synced chain {len(chain)} blocks -> embassy/public/")
PY
python3 health.py
cp pond-health.json embassy/public/ 2>/dev/null || true
cp LAST.txt embassy/public/ 2>/dev/null || true
cp SHA256.txt embassy/public/ 2>/dev/null || true
git add chain.json LAST.txt SHA256.txt embassy/public/chain.json embassy/public/blocks.json embassy/public/pond-health.json embassy/vercel.json embassy/vite.config.js embassy/src/App.jsx 2>/dev/null || true
git diff --cached --quiet || git commit -m "embassy sync $(date -u +%Y-%m-%dT%H:%M:%SZ) #$(jq length chain.json)"
git push
echo "[embassy] pushed"
