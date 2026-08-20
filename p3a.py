import numpy as np
import matplotlib.pyplot as plt

#parámetros
V0 = 0.0
rho0 = 100.0
epsilon = 1.0
omega = 1.85
N = 100
tol = 1e-5
historial = []
V = np.zeros((N, N))
rho = np.zeros((N, N))

# Condiciones de frontera
V[0, :] = V[N - 1, :] = V[:, 0] = V[:, N - 1] = 0
rho[15:35, 15:35] = rho0 
rho[15:35, 65:85] = - rho0
rho[65:86, 15:35] = - rho0
rho[65:85, 65:85] = rho0

# implementación de wawa
for iteration in range(10000):
    V_old = V.copy()
    for i in range(1, N - 1):
        for j in range(1, N - 1):
            if (np.sqrt((i - 50) ** 2 + (j - 50) ** 2) < 35):
                V[i, j] = 0
            else: 
                V_gs = 0.25 * (V[i - 1, j] + V[i + 1, j] + V[i, j + 1] + V[i, j - 1]) + rho[i, j] / (epsilon)
                V[i, j] = (1.0 - omega) * V[i, j] + omega * V_gs


    error = np.max(np.abs(V - V_old))
    historial.append(error)
    if iteration % 100 == 0:
        print(iteration, " ", error)

    if error < tol:
        print("Iteración final: ", iteration)
        break

Ex = np.zeros_like(V)
Ey = np.zeros_like(V)

Ex[1: - 1, 1: -1] = -( V[2: , 1: -1] - V[: - 2, 1: - 1]) / 2
Ey[1: -1, 1: -1] = - ( V[1: -1, 2: ] - V[1: -1, : -2]) / 2

Emag = np.sqrt(Ex ** 2 + Ey ** 2)

x = np.arange(N) * 1
y = np.arange(N) * 1

X, Y = np.meshgrid(x, y)

fig = plt.figure(figsize = (10, 6))
ax1 = fig.add_subplot(2, 2, 1, projection = '3d')
ax1.plot_surface(X, Y, V, cmap = 'viridis')
ax2 = fig.add_subplot(2, 2, 2)
ax2.semilogy(historial)
ax2.axhline(tol, color ='red', alpha = 0.7)
ax2.grid(True)
ax3 = fig.add_subplot(2, 2, 3)
ax3.contour(X, Y, V, colors = 'gray')
ax3.quiver(X, Y, Ey, Ex, Emag, cmap = 'plasma')
ax4 = fig.add_subplot(2,2,4)
ax4.contourf(X, Y, V, cmap = 'viridis')
ax4.contour(X, Y, V, colors = 'black')
plt.tight_layout()
plt.show()