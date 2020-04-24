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
c = QubitPlaceholder.register(n)

ro = p.declare('ro', 'BIT', n+1)


for i in range(n):
    if sumando_1[i] == "1":
        p += X(a[n - (i+1)])
for i in range(n):
    if sumando_2[i] == "1":
        p += X(b[n - (i+1)])
        
for i in range(n-1):
    p += CCNOT(a[i], b[i], c[i+1])
    p += CNOT(a[i], b[i])
    p += CCNOT(a[i], b[i], c[i+1])

p += CCNOT(a[n-1], b[n-1], b[n])
p += CNOT(a[n-1], b[n-1])
p += CCNOT(a[n-1], b[n-1], b[n])  

p += CNOT(c[n-1], b[n-1])

for i in range(n-1):
    p += CCNOT(c[(n-2)-i], b[(n-2)-i], c[(n-1)-i])
    p += CNOT(a[(n-2)-i], b[(n-2)-i])
    p += CCNOT(a[(n-2)-i], b[(n-2)-i], c[(n-1)-i])
    
    p += CNOT(c[(n-2)-i], b[(n-2)-i])
    p += CNOT(a[(n-2)-i], b[(n-2)-i])


for i in range(n+1):
    p += MEASURE(b[i], ro[i])

p.wrap_in_numshots_loop(20)

qvm = get_qc(str(2*n+1)+"q-qvm")
job_stats = qvm.run(address_qubits(p))
print(job_stats) 