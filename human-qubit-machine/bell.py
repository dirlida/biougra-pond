# Bell state |00> + |11> with pure python, no guards
import random, math

def h(state):
    # H on first qubit only for 2 qubits
    # |00>,|01>,|10>,|11>
    a,b,c,d = state
    return [(a+c)/math.sqrt(2), (b+d)/math.sqrt(2), (a-c)/math.sqrt(2), (b-d)/math.sqrt(2)]

def cnot(state):
    # CNOT q0 -> q1
    a,b,c,d = state
    return [a,b,d,c] # swaps |10> <-> |11>

state = [1,0,0,0] # |00>
state = h(state)
state = cnot(state)
print("Bell state:", state)
print("Should be ~0.707,0,0,0.707")

counts = {'00':0,'01':0,'10':0,'11':0}
for _ in range(1024):
    r = random.random()
    if r < state[0]**2: counts['00']+=1
    elif r < state[0]**2 + state[1]**2: counts['01']+=1
    elif r < state[0]**2 + state[1]**2 + state[2]**2: counts['10']+=1
    else: counts['11']+=1

print(counts)
