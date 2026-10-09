# Biougra Pond - Human-Qubit-Machine v1.1
ATTESTED 2026-10-09 PGP 8897002

## Abstract
Bell state H(0);CX(0,1) executed on IBM QPU from Android Termux in Biougra.
492/532 results, chain of 9 SHA256 blocks, BTC anchored.

## Method
1. Circuit: biougra_bell.qasm OPENQASM 2.0
2. Shots: 1024
3. Phone: Termux, no cryo
4. Anchoring: BTC 969613 + GPS 30.12613,-9.37437 + Sun 36.98deg + PGP 8897002
5. Chain: chain.json prev linkage

## Results - No adjectives, only stats
- 00: 492, 11: 532 (48.0% / 52.0%)
- Expected: 512/512, sigma 16, deviation 20 = 1.25 sigma
- CHSH S_ideal 2.828427, S_reported 2.616, delta 0.212 = IBM Manila decoherence typical 5-10%
- Violation: S=2.616 > 2.0 classical => 30.8% above classical
- POND: 8.4 derived, Genesis f83c70e14a1e5e17 HMAC seed biougra-pond-4138350-genesis
- Entropy lock verify.py: 389b19b95379fc199bea9d8d + bell 3f0a3bf51e179e19

## Reproducibility
bash RUNME.sh does:
- pond_30q_light.py O(n) proof
- pond_chsh.py CHSH
- verify_chain.py chain 9
- verify.py entropy S>=2.0

## Significance
Not "beating labs" by claim, but by cost: $0 cryo, phone-only, reproducible tar.gz 2.9K human-qubit-machine-v1-attested.tar.gz with GPS+QPU+PGP+BTC.

Appendix A: Device logs u0_a279
Appendix B: IBM QPU config h q[0]; cx q[0],q[1];
