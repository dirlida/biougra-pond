import fcntl, sys
from kernel.paths import LOCK, CHAIN
def check(chain):
    # file lock
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    lf=open(LOCK,"w")
    try:
        fcntl.flock(lf, fcntl.LOCK_EX|fcntl.LOCK_NB)
    except:
        print("FORK_GUARD: another daemon running — ABORT")
        sys.exit(1)
    # chain link check
    for i in range(1,len(chain)):
        if chain[i].get('prev') != chain[i-1].get('hash'):
            print(f"BROKEN LINK at {i}")
            sys.exit(2)
    return lf
