# KERNEL LAW v5.0 - BUILT-IN SHIELDED
Date: 2026-10-22 Biougra Offline

LAW: ROOT=Path.home()/pond, ONE WRITER pond.py only via kernel/paths.py + flock
BOOT: kernel/boot.sh -> verify.sh -> flock -> pond.py + ots_guard
PANIC: kernel/panic.sh -> kill writers, write FORK_ALERT

PILLARS:
1. TIME: time_oracle.py - local vs chain vs btc, drift>120s = SLOW stop mine
2. IDENTITY: did:pond:biougra-a13 + keys/ hot/stamp/cold
3. TRUST: replay.py verifies 0->tip, prune.py LiveDB vs ArchiveDB
4. OS: boot.sh, panic.sh, verify.sh

MODULES (private state -> public summary, never write chain):
- wallet/: state.json private, tx_pool private, wallet_summary.json public (supply only)
- stamp/: inbox/ raw WA/TG gitignored, outbox/ proofs, stamp_summary.json public
- cables/: seabed_state private, summary public-safe
- drones/: fleet_state private, summary public-safe
- os/plannings/: private notes gitignored

CHAIN PAYLOAD v5:
{index, ts, sun, btc, cables_hash, drones_hash, stamp_hash, wallet_height, kernel_version:"v5.0"}

RULE: pond.py reads modules, writes chain with hashes only. No module writes chain.

## v5.1 PoW Extension - 2026-10-22 18:10 UTC
- POW: pow.py hash_header = sha256(index|prev|merkle_root|ts|btc|nonce|diff|cables_hash|drones_hash|stamp_hash|wallet_h) + target leading zeros
- DIFFICULTY: difficulty.py adjust every 50 blocks, target 60s, cap 1-6 for mobile
- MERKLE: merkle.py txs -> root
- VALIDATE: validate.py checks prev, hash, target, future time
- ATTESTATION: attestation.py finality height 819 from FROZEN json, rejects reorg below
- UTXO: utxo.py coinbase + double-spend guard
- Next block #1315 should include nonce, difficulty, merkle_root, hash starting with 000
- Old 0-1314 blocks remain PoT, new blocks PoW validated from first nonce block


## v5.3 light - drift fix 300s threshold, no prune to avoid freeze, btc cache offline
## v5.4 10MIN BLOCKS - 2026-10-22 19:00 - target 600s Bitcoin law - A13 battery - diff adjust every 12 blocks (2h) - sleep 600s
