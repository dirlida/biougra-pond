import os, fcntl
LOCK_FILE = "/tmp/pond.lock"
CAP_DIFF = 3
SOFT=120
HARD=600
_fd=None
def check_no_doubler():
    global _fd
    try:
        _fd=os.open(LOCK_FILE, os.O_RDWR|os.O_CREAT, 0o600)
        fcntl.flock(_fd, fcntl.LOCK_EX|fcntl.LOCK_NB)
        os.ftruncate(_fd,0); os.write(_fd, str(os.getpid()).encode())
        return True
    except: return False
def check_count(p,c): return c==p+1
def check_diff(d): return CAP_DIFF if d>CAP_DIFF else d
def check_drift(drift):
    import time
    if drift>HARD:
        time.sleep(HARD)
        return False
    if drift>SOFT:
        time.sleep(drift-SOFT)
    return True
