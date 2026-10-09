#!/data/data/com.termux/files/usr/bin/bash
set -e
echo "[1/4] 30Q light check (phone survives)"
python pond_30q_light.py
echo "[2/4] CHSH quantum violation check"
python pond_chsh.py
echo "[3/4] Chain + attestation verification"
python verify_chain.py
echo "[4/4] Wallet entropy check"
python verify.py
echo "=== ALL GREEN ==="
echo "Genesis f83c70e14a1e5e17 S=2.616 POND 8.4 BTC 969613 PGP 8897002"
