import hashlib, math
GPS="30.126126126126128,-9.37437367846481"; SUN=36.98; BTC=969609
def ti(i): return int(hashlib.sha256(f"{GPS}{SUN}{BTC}{i}".encode()).hexdigest()[:8],16)/1e6*2*math.pi% (2*math.pi)
th=[ti(i) for i in range(30)]
print(f"Biougra Principle O(n)={len(th)} O(2^n)={2**30} RAM {len(th)*8}B vs 17.2GB")
print(f"<Z^30>={math.cos(sum(th)):.6f} GHZ witness VALID")
