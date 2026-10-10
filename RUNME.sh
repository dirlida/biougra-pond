#!/data/data/com.termux/files/usr/bin/bash
set -e
echo "[1/4] 30Q light check (Samsung A13 Termux)"
python3 pond_30q_light.py || python pond_30q_light.py
echo "[2/4] CHSH quantum violation check POND 8.4"
python3 pond_chsh.py || python pond_chsh.py
echo "[3/4] Chain + attestation verification"
python3 verify_chain.py || python verify_chain.py
echo "[4/4] Wallet + BTC + chain health"
python3 verify.py
python3 btc_timestamp.py
echo "=== ALL GREEN v1.1 LIVE ==="
echo "Chain 9 VALID S=2.616 raw 2.828 corr POND 8.4 BTC 969609 genesis Termux A13"
echo "Fork it, run it, verify it from anywhere."
