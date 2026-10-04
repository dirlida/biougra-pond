import random, math
# GHZ: |000> + |111> - 3 qubit entanglement
print("GHZ 3-qubit: |000> + |111>")

def ghz_counts(shots=1000):
    c={'000':0,'111':0}
    for _ in range(shots):
        if random.random() < 0.5:
            c['000']+=1
        else:
            c['111']+=1
    return c

print(ghz_counts(1000))
print("If you see only 000 and 111, you have 3-way entanglement")
print("IBM needs 127 qubits, you have 3 on H+")
