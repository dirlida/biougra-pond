#!/data/data/com.termux/files/usr/bin/bash
cd ~/pond
# build without killing hammer
echo "building docs..."
python3 pond.py || true
echo "build done - hammer untouched"
ps aux | grep hammer | grep -v grep
