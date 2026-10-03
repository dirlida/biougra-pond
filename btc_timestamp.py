import hashlib
# Your genesis kernel to timestamp on Bitcoin
kernel = "8fcf242b678b44a7e96f8fd9f7ec570be30880338f3890e9940163e5bdeeee05:Biougra:30.12613,-9.37437:sun36.98:btc969613"
sha = hashlib.sha256(kernel.encode()).hexdigest()
print("OP_RETURN data:")
print(sha)
print("\nTo timestamp: use Sparrow/Electrum wallet, send 0 sats to yourself with OP_RETURN", sha[:64])
print("Cost: ~$0.50. Once mined, your invention is in Bitcoin forever.")

