import numpy as np
import matplotlib.pyplot as plt

#parámetros
V0 = 25.0
hbar = 1
m = 1 / 2
a = 1

def Epar(E):
    return np.sqrt(V0 / E) * np.tan(np.sqrt(V0 - E)) - np.sqrt(E)

def Eimmp(E):
    return - np.sqrt(V0 / E) / np.tan(np.sqrt(V0 - E)) - np.sqrt(E)

def bisex(f, a, b, eps = 1e-10, nmax = 200):
    fa = f(a)
    for i in range(nmax):
        c = (a + b) / 2
        fc = f(c)
        if (np.abs(fc) < eps) or (0.5 * np.abs(a - b)) < eps:
            return c
        if fa * fc < 0:
            b = c
        else:
            a = c
            fa = fc
    return (a + b) / 2

nscan = 20000
escan = np.linspace(1e-6, V0 - 1e-6, nscan)

umbral = 50.0
rpar = np.array([])
rimpar = np.array([])

for i in range(nscan - 1):
    a_s, b_s = escan[i], escan[i + 1]
    fpa, fpb = Epar(a_s), Epar(b_s)
    if (fpa * fpb < 0) and (np.abs(fpa - fpb) < umbral):
        rpar = np.append(rpar, bisex(Epar, a_s, b_s))
        print(bisex(Epar, a_s, b_s))
    fia, fib = Eimmp(a_s), Eimmp(b_s)
    if (fia * fib < 0) and (np.abs(fia - fib) < umbral):
        rimpar = np.append(rimpar, bisex(Eimmp, a_s, b_s))
        print(bisex(Eimmp, a_s, b_s))
Eng2 = Epar(rpar)
Eng1 = Eimmp(rimpar)
print(rpar, "\n", rimpar)
plt.ylim(-20, 20)
plt.scatter(rpar, Eng2)
plt.plot(escan, Eimmp(escan))
plt.plot(escan, Epar(escan))
plt.scatter(rimpar, Eng1)
plt.grid()
plt.show()
