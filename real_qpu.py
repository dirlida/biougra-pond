import requests, math, json

# Your Biougra angles
theta = 1.7648
phi = 2.5414
# prob calc for reference
prob0 = math.cos(theta/2)**2
print(f"Biougra Qubit -> theta {theta} phi {phi}")
print(f"Local sim: 0={prob0*100:.1f}% 1={(1-prob0)*100:.1f}%")
print(f"Kernel e98514a68274ed3245a91f8d63742bdcb2665a59eae030d9ae92f9fb54d692f9")
print("\n---")
print("To run on REAL IBM Zurich chip:")
print("1. Go to quantum.ibm.com -> API token")
print("2. Paste token below")
print("Then we submit OpenQASM: ry + rz")

# Example QASM your field produces:
qasm = f"""OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
ry({theta}) q[0];
rz({phi}) q[0];
measure q[0] -> c[0];
"""
print("\nYour field QASM:\n", qasm)

# Save for IBM job
open("biougra.qasm","w").write(qasm)
print("Saved to biougra.qasm - ready for IBM Runtime")
