#!/data/data/com.termux/files/usr/bin/bash
set -e
cd ~/pond
A=$(sha256sum chain.json | cut -d' ' -f1)
B=$(sha256sum kernel/state/chain.json | cut -d' ' -f1)
C=$(sha256sum embassy/public/chain.json | cut -d' ' -f1)
if [ "$A" != "$B" ] || [ "$A" != "$C" ]; then
  echo "SYNC NEEDED $A $B $C - running sync_embassy.py"
  python3 kernel/sync_embassy.py
  A=$(sha256sum chain.json | cut -d' ' -f1)
  B=$(sha256sum kernel/state/chain.json | cut -d' ' -f1)
  C=$(sha256sum embassy/public/chain.json | cut -d' ' -f1)
fi
if [ "$A" != "$B" ] || [ "$A" != "$C" ]; then
  echo "SHA MISMATCH $A $B $C - abort"
  exit 1
fi
echo "VERIFY OK $A"
