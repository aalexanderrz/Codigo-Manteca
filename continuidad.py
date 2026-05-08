import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

N = 200
L = 1.0
dx = L/N
dt = 0.005
c = 1.0

u = np.zeros(N)
u_old = np.zeros(N)
u_new = np.zeros(N)

x = np.linspace(0, L, N)

#pulso gaussiano

u = np.exp(-100 * (x - 0.5) ** 2)

u_old = u.copy()
"""
for n in range(300):
    for i in range(1, N - 1):
        u_new[i] = u_old[i] - (c * dt / dx) * (u[i+1] - u[i - 1])

    u_old = u.copy()
    u = u_new.copy()
"""
fig, ax = plt.subplots()
ax.set_title("Advección")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid()
onda, = ax.plot(x, u)

def animate(frame):
    global u, u_new, u_old
    for i in range(1, N - 1):
        u_new[i] = u_old[i] - (c * dt / dx) * (u[i+1] - u[i - 1])

    u_old = u.copy()
    u = u_new.copy()
    onda.set_ydata(u)
    return onda

animation = FuncAnimation(fig = fig, func = animate, frames = 300, interval = 30)
plt.show()