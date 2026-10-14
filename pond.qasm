OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
ry(1.7648) q[0];
rz(2.5414) q[0];
measure q[0] -> c[0];
