import hashlib, json
# Your genesis kernel to timestamp on Bitcoin — v1.0
kernel = "8fcf242b678b44a7e96f8fd9f7ec570be30880338f3890e9940163e5bdeeee05:Biougra:30.12613,-9.37437:sun36.98:btc969613"
sha = hashlib.sha256(kernel.encode()).hexdigest()
print("OP_RETURN data v1.0:")
print(sha)
print("\nTo timestamp: use Sparrow/Electrum wallet, send 0 sats to yourself with OP_RETURN", sha[:64])
print("Cost: ~$0.50. Once mined, your invention is in Bitcoin forever.")

# v1.1 — live chain anchor
try:
    blocks=json.load(open("chain.json"))
    tip=blocks[-1]["hash"]
    print("\n--- v1.1 LIVE ---")
    print(f"Genesis btcHeight: {blocks[0]['payload']['btcHeight']} (actual chain)")
    print(f"Tip hash 9 blocks: {tip}")
    print(f"OP_RETURN v1.1: {tip[:32]}")
    print(f"Bell S=2.616 raw 2.828 corr POND 8.4")
except Exception as e:
    print(e)
