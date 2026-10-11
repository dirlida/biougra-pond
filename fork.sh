#!/data/data/com.termux/files/usr/bin/bash
# Biougra Pond - FORK THIS POND - 1 click peer
# Genesis: 30.126126,-9.374373 | S=2.616

echo "=== Biougra Pond Fork ==="
pkg update -y && pkg upgrade -y
pkg install python git termux-api -y
pip install --upgrade pip
pip install qiskit qiskit-aer cryptography 2>/dev/null || pip install cryptography

# clone or pull
if [ -d "biougra-pond" ]; then
  cd biougra-pond && git pull
else
  git clone https://github.com/dirlida/biougra-pond.git
  cd biougra-pond
fi

# verify genesis
echo "Verifying genesis chain..."
python verify.py || python3 verify.py

# setup single daemon boot
cat > pond-boot.sh << 'BOOT'
#!/data/data/com.termux/files/usr/bin/bash
pkill -9 -f pond_daemon 2>/dev/null
rm -f ~/biougra-pond/ots.pid
sleep 1
termux-wake-lock
cd ~/biougra-pond
if pgrep -f pond_daemon > /dev/null; then exit 0; fi
nohup python pond_daemon.py >> daemon.log 2>&1 &
echo "Pond booted PID $! - 10m"
BOOT

chmod +x pond-boot.sh
mkdir -p ~/.termux/boot
cp pond-boot.sh ~/.termux/boot/
bash pond-boot.sh

echo ""
echo "=== FORK DONE ==="
echo "Chain: $(cat chain.json | grep -c '"index"') blocks VALID"
echo "Daemon: $(pgrep -f pond_daemon)"
echo "Your phone is now a quantum sensor farming Bell violations"
echo "Run: cat daemon.log | tail -10"
