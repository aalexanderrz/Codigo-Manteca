import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

N = 250
dx = 0.4
dt = 0.05
eps = 0.2
mu = 0.1
Nt = 200

x = np.arange(N)*dx
t_vals = np.arange(Nt) * dt
np.random.seed(0)
u = 0.2 * np.random.rand(N)

#Suavizado leve
u = (np.roll(u,1) + u + np.roll(u,-1)) / 3
u_old = u.copy()
u_new = np.zeros_like(u)

#almacenamiento 3d
U = np.zeros((Nt, N))

#Evolución KdV
for n in range(Nt):

    for i in range(2, N - 2):
        nonlinear = (u[i + 1] + u[i] + u[i - 1]) * (u[i + 1] - u[i - 1])
        dispersion = (u[i + 2] + 2 * u[i - 1] - 2 * u[i + 1]- u[i - 2])

        u_new[i] = (u_old[i] - eps * dt / (3 * dx) * nonlinear - mu * dt / (dx ** 3) * dispersion)

    #condiciones de frontera
    u_new[0:2] = 0
    u_new[-2:] = 0

    u_old = u.copy()
    u = u_new.copy()

    U[n, :] = u

X, T = np.meshgrid(x, t_vals)

fig = plt.figure(figsize = (10,7))
ax = fig.add_subplot(111, projection = '3d')

surf = ax.plot_surface(X, T, U, cmap = 'viridis', linewidth = 0, antialiased = True)

ax.set_xlabel("Posición x")
ax.set_ylabel("Tiempo t")
ax.set_zlabel("u(x,t)")
ax.set_title("Emergencia de solitones desde ruido (KdV)")

fig.colorbar(surf, shrink = 0.5, aspect = 10, label = "Amplitud")

plt.show()
