import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#parámetros físicos
c = 1
Nz = 400 #puntos espaciales
dz = 1 #paso expacial
beta = 0.4 #condición de courant
dt = beta * dz / c
lambda0 = 30
k = 2 * np.pi / lambda0
steps  = 600
phase = 2 * np.pi / 3

Ex = np.zeros(Nz)
Hy = np.zeros(Nz)

#pulso inicial gausiano
z = np.arange(Nz)

Ex = np.exp(-((z - 80) / 15) ** 2) * np.sin(k * z)
Hy = np.exp(-((z - 80) / 15) ** 2) * np.sin(k * z + phase ) / c

fig, ax = plt.subplots(figsize = (10, 5))

lineE, = ax.plot(z, Ex, label = r'E_x')
lineH, = ax.plot(z, Hy, label = r'H_y')

ax.set_xlim(0, Nz)
ax.set_ylim(-1.2, 1.2)

ax.legend()

def update(frame):

    global Ex, Hy

    #actualizar Ex
    Ex[1:-1] += beta * (Hy[:-2] - Hy[1:-1])

    #Actualizar Hy
    Hy[1:-1] += beta * (Ex[1:-1] - Ex[2:])

    #condiciones de frontera
    Ex[0] = Ex[-1] = 0
    Hy[0] = Hy[-1] = 0

    lineE.set_ydata(Ex)
    lineH.set_ydata(Hy)

    return lineE, lineH
ani = FuncAnimation(fig, update, frames = steps, interval = 20, blit = True)
plt.show()