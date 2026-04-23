import numpy as np
import matplotlib.pyplot as plt

x0 = np.array([0,4],float)
k = 0
w = 0.8
t0 = 0
tf = 30
N = 1000
h = (tf - t0) / N

def f(x):
        dvdt = -k*x[1] - (w**2)*x[0]
        dxdt = x[1]
        return np.array([dxdt, dvdt],float)

def euler(x, f):
    return x + h*f(x)

tpoints = np.arange(t0, tf, h)
xan = (x0[0] * np.cos(w * tpoints) + x0[1] * np.sin(w * tpoints) / w)
van = (- w * x0[0] * np.sin(w * tpoints) + x0[1] * np.cos(w * tpoints))
x = np.zeros(N)
v = np.zeros(N)
x[0] = x0[0]
v[0] = x0[1]
for i in range(1,N):
    x[i] = euler(x0, f)[0]
    v[i] = euler(x0, f)[1]
    x0 = np.array([x[i],v[i]], float)

fig, ax = plt.subplots(1,2, figsize = (12,4))
ax[0].plot(tpoints, x, label = 'numérica', color = 'green')
ax[0].plot(tpoints, xan, label = 'analítica', color = 'red')
ax[0].legend()
ax[0].grid()
ax[1].plot(tpoints,v, label = 'numérica', color = 'black')
ax[1].plot(tpoints, van, label ='analítica', color = 'blue')
ax[1].legend()
ax[1].grid()
plt.show()