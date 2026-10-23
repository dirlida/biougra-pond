# Pond Embassy — Biougra Sovereign Chain

Biougra A13 phone mined, 10min blocks, 000 minimum, built for longevity.

Pond is a phone-native blockchain running 24/7 on a Samsung A13 in Termux. No VPS, no ASIC. Designed to run non-stop for years on low CPU/GPU, not hours.

### Core Intent
- Longevity over flex: Locked at 000 (diff 3) - never drops to 00. Phone stays cool, chain never stalls.
- Binary quantum qubit kernel: Minimal consensus kernel/consensus/ - pow.py, difficulty.py, validate.py, light_client.py - clean, auditable, no bloat.
- Proof of phone: First 0000 ever mined on A13: 000017d9 #1342 nonce 76384 (commit 83f27f2). Current chain: 00011bc80253fba9 #1403 + 000ddf3d #1404 both diff 3.

### What Judges See
- Chain: chain.json 1405 blocks, 760KB
- Light headers: embassy/dist/headers.json 76KB - 5x smaller for slow data
- Status: embassy/dist/status.json - height, last hash, verify OK
- Legends: embassy/dist/legends.json - Hall of Fame quad-zero
- Verify: ./kernel/verify.sh - binary checks

### Why 000?
- 00 = 8 bits, too easy, spam risk
- 000 = 12 bits, ~4096 hashes avg - perfect for phone longevity
- 0000 = 16 bits, ~65536 hashes - we did it, proof in logs, but thermal kills long runs
- 00000 = 20 bits, ~1M hashes - 2-3h on A13, possible for one-shot, kills 10min rhythm
- 000000 = 24 bits, ~16M hashes - 20h+, not viable for this build

We choose 000. Other builds can jack numbers. This one is for unbreakable chaining, human + device running day in day out.

### Run
python3 pond.py
python3 kernel/consensus/difficulty.py
./kernel/verify.sh

Built in Biougra, Souss, MA - A13 4GB, Termux, Oct 2026.
