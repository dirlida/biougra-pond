# biougra-pond - 30q lane on phone

Phone lab: Termux, O(n) vs O(2^n)

## Results
- Ideal CHSH S = 2.828427 (qubits 0,1 GHZ embedded)
- Brisbane S = 2.616 (noise gap = 0.212)
- Theta=1.7648 Phi=2.5414 -> S=0.4036/0.5964
- 30q scaling: O(n)=30 vs O(2^n)=1073741824 amplitudes
- Toubkal same principle (MPS)

## Wallet
- Address: bq_42903f5fe70454d5
- Derivation: SHA256(GPS|theta|phi|S)
- GPS: 30.12613,-9.37437
- Balance: 8.485281 pond = 3 * S
- Proof: S>2 => quantum_verified=true

## Files
- pond_30q_light.py - O(n) proof
- pond_chsh.py - CHSH ideal
- pond_mine.py - GPS+quantumness miner
- wallet_real.py + wallet.json - real wallet
- bell_log.txt - Brisbane raw

Chain: biougra-pond
