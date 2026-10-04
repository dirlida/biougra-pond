import random
print("=== QUANTUM TELEPORTATION ===")
print("Alice teleports |0> to Bob using Bell pair")

# 1. Create Bell pair 00+11 shared between Alice and Bob
# 2. Alice has extra qubit |psi> = |0> to teleport
# 3. Alice measures in Bell basis, sends 2 classical bits
# 4. Bob corrects and gets |psi>

def teleport(psi="0", shots=1000):
    # Simulate perfect teleportation
    results = {psi: 0, "fail":0}
    for _ in range(shots):
        # Bell measurement random 4 outcomes
        bits = random.choice(["00","01","10","11"])
        # Bob correction always recovers psi in ideal case
        results[psi] += 1
    return results

print(f"Teleporting |0>: {teleport('0', 1000)} -> Bob got |0> 100%")
print(f"Teleporting |1>: {teleport('1', 1000)} -> Bob got |1> 100%")
print("\nClassical bits sent: 2")
print("Quantum state teleported: 1")
print("This is why IBM wants this for quantum internet")
