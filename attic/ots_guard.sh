#!/data/data/com.termux/files/usr/bin/bash
POND_DIR="$HOME/pond"
ATTIC="$POND_DIR/attic/ots"
mkdir -p "$ATTIC"
while true; do
  mv -n "$POND_DIR"/*.ots "$ATTIC"/ 2>/dev/null
  mv -n "$POND_DIR"/chain.json.ots.* "$ATTIC"/ 2>/dev/null
  mv -n "$POND_DIR"/chain.json.ots.pending "$ATTIC"/ 2>/dev/null
  mv -n "$POND_DIR"/chain.json.ots.tmp "$ATTIC"/ 2>/dev/null
  sleep 15
done
