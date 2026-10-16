#!/data/data/com.termux/files/usr/bin/bash
# if termux wipes, run this to rebirth
cd ~
mkdir -p pond
cd pond
cp /sdcard/PondEmbassy/*. 2>/dev/null || cp /sdcard/Download/pond-chain.json chain.json
echo "reborn from sdcard"
python verify.py
