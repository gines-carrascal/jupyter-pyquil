from pyquil import get_qc, Program
from pyquil.gates import H, X, CPHASE, MEASURE
from pyquil.latex import to_latex, display
from pyquil.quil import address_qubits
from pyquil.quilatom import QubitPlaceholder
from math import pi

sumando_1 = input("Primer sumando en binario (4 bits)")
sumando_2 = input("Segundo sumando en binario(4 bits)")

n = 4

n+=1

p = Program()


a = QubitPlaceholder.register(n)
b = QubitPlaceholder.register(n)

ro = p.declare('ro', 'BIT', n)

for i in range(1,n):
    if sumando_1[i-1] == "1":
        p += X(a[n - (i+1)])
for i in range(1,n):
    if sumando_2[i-1] == "1":
        p += X(b[n - (i+1)])
        
# Take the QFT.
# Iterate through the target.
for i in range(n,0,-1):
    # Apply the Hadamard gate to the target.
    p += H(b[i-1])

    # Iterate through the control.
    for j in range(i-1,0,-1):
        p += CPHASE(2*pi/2**(i-j+1), b[j-1], b[i-1])
        
# Compute controlled-phases.
# Iterate through the targets.
for i in range(n,0,-1):
    # Iterate through the controls.
    for j in range(i,0,-1):
        p += CPHASE(2*pi/2**(i-j+1), a[j-1], b[i-1])

# Take the inverse QFT.
# Iterate through the target.
for i in range(1,n+1):
    # Iterate through the control.
    for j in range(1,i):
        # The inverse Fourier transform just uses a negative phase.
        p += CPHASE(-2*pi/2**(i-j+1), b[j-1], b[i-1])

    # Apply the Hadamard gate to the target.
    p += H(b[i-1])


for i in range(n):
    p += MEASURE(b[i], ro[i])

p.wrap_in_numshots_loop(20)

print(address_qubits(p)) 


p.wrap_in_numshots_loop(20)

qvm = get_qc(str(2*n+1)+"q-qvm")
job_stats = qvm.run(address_qubits(p))
print(job_stats) 