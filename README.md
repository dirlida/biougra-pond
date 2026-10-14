# THE COUNT — Biougra Pond

A time-counting chain born in Biougra, Souss-Massa, Morocco.

Not a coin. Not a token. Just proof that time passed, and we were there to count it.

## How It Works

- Daemon creates a new block every 10 minutes
- Each block contains: index, timestamp, previous hash, hash
- verify.py checks the whole chain — hash links + timing

Rule active from block 36: Every block must be at least 10 minutes after the previous block. No exceptions.

Run: python verify.py

## Genesis & Location Disclaimer

THE COUNT genesis block contains an approximate GPS coordinate for symbolic birthplace purposes only.

- This coordinate is approximate and falls within the general farm area in Biougra, Souss-Massa. It is not a precise location, not a building, and not a claim to any specific structure.
- This is NOT a land deed, NOT a property claim, NOT a title (titre foncier / melkia). Land in this area is under traditional Melkia indivision with multiple heirs, and no single individual holds clean sole ownership.
- THE COUNT is an independent time-counting experiment. It does not belong to any landowner, farm, or family. Location of genesis does not equal ownership.
- Blocks after genesis contain no location data — only time and hash.

## Portability

THE COUNT is already portable and already location-free after genesis.

- Block 0 has GPS. Blocks after genesis have no GPS.
- The chain continues counting regardless of where it runs.
- Moving location does not stop THE COUNT, and does not transfer ownership to anyone.

Born in Biougra. Lives wherever it runs.
