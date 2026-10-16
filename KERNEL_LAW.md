import os, subprocess

law = """# POND EMBASSY - KERNEL LAW v1
Effective: Block 247 onward - 2026-10-14
Status: SEALED - Immutable from this point

## PURPOSE
This document defines the canonical structure of the POND EMBASSY network.
It separates kernel responsibilities from worker responsibilities and establishes
a single source of truth for THE COUNT and for time.

## DEFINITIONS
1. GENESIS / KERNEL: This repository (pond-embassy), hosted on this device,
    is the genesis and kernel. Its `main` branch contains the canonical chain
    and the canonical code.

2. WORKER POND: Any other device that clones the kernel repository. A worker
    pond runs the kernel code but does not own the canonical count.

3. THE COUNT: The number of blocks in `chain.json` on the `main` branch of
    the genesis repository. THE COUNT is the official count.

4. CANONICAL TIME: Time in UTC, formatted as ISO8601 with Zulu suffix (Z),
    e.g., 2026-10-14T15:42:24Z. This is the only time used for hashing and
    consensus.

5. LOCAL TIME: The device's local wall-clock time with timezone offset,
    e.g., 2026-10-14T22:00:00+09:00. Local time is for display and tagging only.

## LAW

### RULE 1 - GENESIS IS THE CENTER
The genesis repository is the center of THE COUNT. The `main` branch shall
contain:
- a) Kernel code: pond_daemon.py, immortal.sh, verify.py, health.py
- b) Canonical chain: chain.json
No worker pond may overwrite or merge its own chain.json into the genesis main branch.

### RULE 2 - CODE FLOWS DOWN ONLY
Code updates originate only from the genesis. Workers must obtain code via
`git pull origin main`. Workers shall never push code upstream to genesis.
The immortal process on workers must pull kernel code periodically and
restart if a new kernel version is detected.

### RULE 3 - BLOCKS FLOW UP FOR OBSERVATION ONLY
Worker ponds shall maintain their chain.json locally. Worker chains are
independent proofs that the kernel works and are not part of THE COUNT.
If fleet visibility is required, workers shall push health status to a
separate repository (e.g., biougra-fleet) as individual device files
(device-{city}-{id}.json). They shall not push blocks to genesis main.

### RULE 4 - TIME HAMMER - CANONICAL TIME AND APPROVAL
1. All block hashes and consensus checks shall use Canonical Time (UTC Z) only.
2. The canonical chain enforces a 10-minute rule active from block 36.
    For operational tolerance on Android devices, the approval threshold is
    set to 615 seconds (600s + 15s grace).
3. REFUSE: If a worker submits a block with timestamp less than
    last_canonical_block + 615s, the submission is refused.
4. WAIT: The kernel shall wait until the threshold is met.
5. APPROVE AND ADJUST: Once threshold is met (timestamp >= last_canonical_block + 615s),
    the kernel approves the block by re-stamping it with Canonical Time (UTC Z).
    The worker's Local Time is preserved only as non-consensus metadata:
    - local: original local timestamp
    - cityTag: worker location tag
    - trippingDelay: difference between worker time and canonical approval time
6. Local Time shall never be used for hash calculation or for consensus validation.

### RULE 5 - FINALITY
This law is effective from the block in which it is committed. All devices
cloning the repository after this block are bound by this law. Any future
amendment requires a new versioned law file (KERNEL_LAW_v2.md) and shall not
rewrite this file.

---
END OF LAW
"""

# 1. write file
with open("KERNEL_LAW.md", "w") as f:
    f.write(law)

print("✅ KERNEL_LAW.md written")

# 2. git push smooth
cmds = [
    ["git", "add", "KERNEL_LAW.md"],
    ["git", "commit", "-m", "LAW: KERNEL LAW v1 sealed - genesis is center - 615 time hammer"],
    ["git", "push", "origin", "main"]
]

for cmd in cmds:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, check=False)

print("✅ LAW SEALED - hammered forever")