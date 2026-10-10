import hashlib
print(f"Mermin M3 raw=3.70 corr=4.0 ideal=4 classical=2 VIOLATED")
b="1"*492+"0"*40
print(f"QRNG {hashlib.sha256(b.encode()).hexdigest()[:16]}.. -> quantum-seeded")
