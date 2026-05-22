import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#parámetros físicos
c = 1e8
mu0 = 4*np.pi*1e-7
eps0 = 1 / (mu0 * c ** 2)


Nz = 400
dz = 1e-3

dt = dz / (2 * c)

Nt = 1500
steps = 1500

z1 = 250
z2 = 350

Ex = np.zeros(Nz)
Hy = np.zeros(Nz)
eps_r = np.ones(Nz)
eps = eps_r * eps0

n = 2.0

eps_r[z1:z2] = n ** 2

z = np.arange(Nz)

z0 = 80
sigma = 20

lambda0 = 40

k = 2 * np.pi / lambda0

Ex = np.exp(-(z - z0) ** 2 / (2 * sigma ** 2)) * np.sin(k * z)

fig, ax = plt.subplots(figsize = (11, 5))

line1, = ax.plot(z, Ex, label = r'E_x')
line2, = ax.plot(z, Hy, label = r'H_y')

ax.axvspan(z1, z2, alpha = 0.2)

ax.set_xlim(0, Nz)
ax.set_ylim(-1.5, 1.5)

ax.grid()
ax.legend()

def update(frame):

    global Ex, Hy
    for i in range(Nz - 1):
        Hy[i] = Hy[i] + (dt / (mu0 * dz)) * (Ex[i + 1] - Ex[i])

    for i in range(1, Nz):
        Ex[i] = Ex[i] + (dt / (eps0 * eps_r[i] * dz)) * (Hy[i] - Hy[i-1])
    
    Ex[0] = 0
    Ex[-1] = 0

    line1.set_ydata(Ex)
    line2.set_ydata(Hy)

    return line1, line2
ani = FuncAnimation(fig, update, frames = steps, interval = 20, blit = True)
plt.show()