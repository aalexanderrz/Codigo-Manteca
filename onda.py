# 14/04/2026
# Clase sobre PDEs

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#parámetros físicos
L = 1.0
c = 1.0

#Discretización
Nx = 200
dx = L / (Nx -1)

dt = 0.004
Nt = 600
courant = c * dt / dx
#malla espacial
x = np.linspace(0, L, Nx)

#Inicialización
y = np.zeros((Nt, Nx))

#Condición inicial
y[1, :] = np.exp(- 100 * (x-0.5) ** 2) #np.where((x > 0.4) & (x < 0.6), 1.0, 0.0)
#np.sin(np.pi * x / L) 

#Velocidad inicial nula
y[0, :] = y[1, :]

#Evolución temporal (leapfrog)

for j in range(1, Nt - 1):
    for i in range(1, Nx -1):
        y[j + 1, i] = (2 * y[j, i] - y[j - 1, i] + (courant ** 2) * (y[j, i + 1] + y[j, i-1] -2 * y[j, i]))

        # Condiciones de frontera
        y[j + 1, 0] = 0
        y[j + 1, -1] = 0

#modos de fourier
def fourier_modes(x, t, L, N):
    yf = np.zeros_like(x)
    for n in range(1, N + 1):
        Bn = 2 * np.trapezoid(np.exp(- 100 * (x - 0.5) ** 2) * np.sin(n * np.pi * x) , x ) / L
        wn = n * np.pi * c / L
        yf += Bn * np.sin(n * np.pi * x / L) * np.cos(wn * t)
    return yf

t_index = 200
t_val = t_index * dt

y_fourier = fourier_modes(x, t_val, L, 10)
plt.plot(x, y[t_index, :], label = "Leapfrog")
plt.plot(x, y_fourier, '--', label = "Modos")
plt.legend()
plt.grid()

"""
#intento de animar
fig, ax = plt.subplots()
ax.set_ylim(-1.01,1.01)
onda, = ax.plot(x,y[0,:])

def animate(frame):
    onda.set_data(x, y[3 * frame,:])
    return onda

animacion = FuncAnimation(fig = fig, func=animate, frames = Nt, interval = 10)
animacion.save('onda.gif')
"""
plt.show()
