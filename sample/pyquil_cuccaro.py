from pyquil import get_qc, Program
from pyquil.gates import X, CNOT, CCNOT, MEASURE
from pyquil.latex import to_latex, display
from pyquil.quil import address_qubits
from pyquil.quilatom import QubitPlaceholder

sumando_1 = input("Primer sumando en binario (4 bits)")
sumando_2 = input("Segundo sumando en binario(4 bits)")

n = 4

p = Program()


a = QubitPlaceholder.register(n)
b = QubitPlaceholder.register(n+1)
c = QubitPlaceholder.register(1)

ro = p.declare('ro', 'BIT', n+1)

for i in range(n):
    if sumando_1[i] == "1":
        p += X(a[n - (i+1)])
for i in range(n):
    if sumando_2[i] == "1":
        p += X(b[n - (i+1)])

for i in range(1, n):
    p += CNOT(a[i], b[i])

p += CNOT(a[1], c[0])

p += CCNOT(a[0], b[0], c[0])
p += CNOT(a[2], a[1])

p += CCNOT(c[0], b[1], a[1])
p += CNOT(a[3], a[2])

for i in range(2, n-2):
    p += CCNOT(a[i-1], b[i], a[i])
    p += CNOT(a[i+2], a[i+1])

p += CCNOT(a[n-3], b[n-2], a[n-2])
p += CNOT(a[n-1], b[n])

p += CCNOT(a[n-2], b[n-1], b[n])
for i in range(1, n-1):
    p += X(b[i])

p += CNOT(c[0], b[1])
for i in range(2, n):
    p += CNOT(a[i-1], b[i])

p += CCNOT(a[n-3], b[n-2], a[n-2])

for i in range(n-3,1,-1):
    p += CCNOT(a[i-1], b[i], a[i])
    p += CNOT(a[i+2], a[i+1])
    p += X(b[i+1])

p += CCNOT(c[0], b[1], a[1])
p += CNOT(a[3], a[2])
p += X(b[2])

p += CCNOT(a[0], b[0], c[0])
p += CNOT(a[2], a[1])
p += X(b[1])

p += CNOT(a[1], c[0])

for i in range(n):
    p += CNOT(a[i], b[i])        
    
for i in range(n+1):
    p += MEASURE(b[i], ro[i])

p.wrap_in_numshots_loop(20)

print(address_qubits(p)) 


p.wrap_in_numshots_loop(20)

qvm = get_qc(str(2*n+1)+"q-qvm")
job_stats = qvm.run(address_qubits(p))
print(job_stats) 