
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

gamma = 1.0 #friccion

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

for j in range(1, Nx -1):
    y[j + 1, 1: -1] = (2 - gamma * dt) * y[j, 1: -1] - (1 - gamma *dt) * y[j - 1, 1: - 1] +(courant ** 2) * (y[j, 2:] + y[j, : -2] -2 * y[j, 1: -1])

    # Condiciones de frontera
    y[j + 1, 0] = 0
    y[j + 1, -1] = 0

#intento de animar
fig, ax = plt.subplots()
ax.set_ylim(-1.2,1.2)
onda, = ax.plot(x,y[0,:])

def animate(frame):
    onda.set_ydata(y[frame, :])
    ax.set_title(f"t = {frame * dt:.3f}")
    return onda,

animacion = FuncAnimation(fig = fig, func=animate, frames = Nt, interval = 20)
#animacion.save('onda.gif')
plt.show()