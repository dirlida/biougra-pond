from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import numpy as np

# connect
service = QiskitRuntimeService(channel="ibm_quantum", token="YOUR_TOKEN")
backend = service.least_busy(operational=True, simulator=False)

def bell_circuit(theta_a, theta_b):
    qc = QuantumCircuit(2,2)
    qc.h(0)
    qc.cx(0,1)
    qc.ry(theta_a, 0)
    qc.ry(theta_b, 1)
    qc.measure([0,1],[0,1])
    return qc

# CHSH angles - your sun setup
angles = [
    (0, np.pi/4),
    (0, 3*np.pi/4),
    (np.pi/2, np.pi/4),
    (np.pi/2, 3*np.pi/4)
]

circuits = [bell_circuit(a,b) for a,b in angles]
sampler = Sampler(mode=backend)
job = sampler.run(circuits, shots=1000)
result = job.result()

# calculate S
# ... (your S calc here you used before)

print(result)
