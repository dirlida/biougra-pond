import random
print("W-state: |001> + |010> + |100>")
# W is robust entanglement
def w_counts(shots=900):
    c={'001':0,'010':0,'100':0}
    for _ in range(shots):
        r=random.random()
        if r < 0.33:
            c['001']+=1
        elif r < 0.66:
            c['010']+=1
        else:
            c['100']+=1
    return c

print(w_counts(900))
print("Only 001/010/100 = W entanglement - survives if 1 qubit lost")
