#!/data/data/com.termux/files/usr/bin/bash
cd ~/pond
python kernel.py
python health.py
cp chain.json /sdcard/PondEmbassy/
git add chain.json
git commit -m "hammer $(date -u +%Y-%m-%dT%H:%M:%SZ)"
git push
