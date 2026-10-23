#!/usr/bin/env python3
import pathlib, time, subprocess, os, glob
ROOT=pathlib.Path.home()/"pond"
LOG=ROOT/"pond.log"
# rotate if >10MB
if LOG.exists() and LOG.stat().st_size > 10*1024*1024:
    for i in range(5,0,-1):
        src=ROOT/f"pond.log.{i-1}" if i>1 else LOG
        dst=ROOT/f"pond.log.{i}"
        if src.exists():
            try: src.rename(dst)
            except: pass
    print("[GUARD] rotated logs")

# ensure single miner
lock=ROOT/"tmp/pond.lock"
if not lock.exists():
    print("[GUARD] lock missing, starting pond")
    subprocess.Popen(["bash","-c","cd ~/pond && nohup python -u pond.py > pond.log 2>&1 &"])
else:
    # check proc alive
    try:
        pid=int(lock.read_text().strip())
        if not pathlib.Path(f"/proc/{pid}").exists():
            print(f"[GUARD] pid {pid} dead, restart")
            lock.unlink()
            subprocess.Popen(["bash","-c","cd ~/pond && nohup python -u pond.py > pond.log 2>&1 &"])
    except: pass

# cable + drone ingest each guard loop
try:
    subprocess.run(["python", str(ROOT/"kernel/modules/cables/ingest.py")], timeout=5)
    subprocess.run(["python", str(ROOT/"kernel/modules/drones/fleet_ingest.py")], timeout=5)
except: pass
