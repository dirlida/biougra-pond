import json, hashlib
chain=json.load(open("chain.json"))
print(f"Chain length: {len(chain)}")
ok=True
for i in range(1,len(chain)):
    if chain[i]['prev']!= chain[i-1]['hash']:
        print(f"FAIL at {i}"); ok=False
    else:
        print(f"OK {i}: {chain[i-1]['hash'][:8]} -> {chain[i]['hash'][:8]}")
print(f"FINAL: {chain[-1]['hash']}")
print(f"PREV FINAL: {chain[-2]['hash']}")
print(f"CHAIN VALID: {ok}")
# check attestation links
att=json.load(open("attestation/ORIGIN.json"))
print(f"ORIGIN btc {att['btcHeight']} genesis {att['genesis']} S {att['entropy']}")
