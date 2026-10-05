# Biougra Pond: Human-Qubit-Machine Protocol
Version 1.0 - October 2026

## Abstract
Biougra Pond is a minimal quantum-anchored timestamping protocol that binds a geographic coordinate, a Bitcoin block height, and a verifiable Bell-state measurement from an IBM Quantum QPU into a hash chain.

## 1. Origin Coordinate
- Location: 30.12613,-9.37437 (Biougra, Morocco)
- Sun elevation: 36.98 at timestamp
- Time: 2026-10-02T16:12:51.736920Z
- BTC Height: 969613

## 2. Quantum Proof
Circuit: biougra.qasm - Bell state preparation H(0); CX(0,1)
Execution: real_qpu.py on IBM Quantum backend
Shots: 1024
Result: {'00': 492, '11': 532}
Verification: Correlated counts confirm entanglement, non-classical distribution.

## 3. Chain Structure
File: chain.json
Fields: pond, gps, gpsStr, btcHeight, prev hash, payload hash
Example hash: ab5446ede0c96a930f31307b92dbf386ea371f13774bb187a116412cb303918f
Prev: 3ae3d838f894c251e5c5abe89e4ef1b4898d52eb40dc318f6f6a6193e74a94a8

## 4. Artifacts
- biougra.qasm: QASM 2.0 Bell circuit
- real_qpu.py: QPU execution script
- qubit_wallet.py: Deterministic wallet derivation from quantum measurement
- chain.json: Sealed chain
- human-qubit-machine.tar.gz: Full reproducible package (13KB)

## 5. Reproducibility
Requirements: Python 3, Qiskit, Linux/Termux environment
Command: python3 real_qpu.py
Expected: Bell distribution approx 50/50

## 6. License and Origin Tax
License: See LICENSE (1.4KB)
Origin Tax: 1% rule defined in ORIGIN.json

## 7. Conclusion
Protocol demonstrates low-resource quantum anchoring achievable on consumer mobile hardware with access to cloud QPUs.
