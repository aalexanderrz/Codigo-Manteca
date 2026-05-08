import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

L = 1.0
nx = 200
dx = L / (nx -1)

#parámetros físicos
rho0 = 0.01
T0 = 40.0
alfa = 0.5
kappa = 100

#malla
x = np.linspace(0, L, nx)

modelo  = "catenaria" # "Catenaria"

if modelo == "exponencial":
    rho = rho0 * np.exp(alfa * x)
    T = T0 * np.exp(alfa * x)

elif modelo == "catenaria":
    g = 9.8
    rho = rho0 * np.ones_like(x)
    T = T0 * np.cosh(rho0 * g * x / T0)


v = np.sqrt(T / rho)
vmax = np.max(v)

#condición de estabilidad
dt = 0.4 * dx / vmax

print("dt = ", dt)

y = np.exp(-200 * (x/5 - 0.25) ** 2) - np.exp(-200 * (x/3 - 0.75) ** 2) + np.exp(-200 * (x/4 - 0.5) ** 2) - np.exp(-200 * (x/5 - 0.15) ** 2) #pulso gaussiano
y_old = y.copy()
y_new = np.zeros(nx)

def step():
    global y, y_old, y_new
    
    for i in range(1, nx -1):
        T_ip = 0.5 * (T[i] + T[i + 1])
        T_im = 0.5 * (T[i] + T[i - 1])

        lap = (T_ip * (y[i + 1] - y[i]) - T_im * (y[i] - y[i -1])) /  dx ** 2

        y_new[i] = (2 * y[i] - y_old[i] + dt ** 2 * lap / rho[i] - kappa * dt * (y[i] - y_old[i]))

    y_new[0] = 0
    y_new[-1] = 0

    y_old[:] = y[:]
    y[:] = y_new[:]

fig, ax = plt.subplots()

line, = ax.plot(x, y)
ax.set_ylim(-1, 1)
ax.set_title(r"Onda con T(x), $\rho (x)$ variables")

def update(frame):
    for _ in range(5):
        step()
    line.set_ydata(y)
    return line,

ani = FuncAnimation(fig, update, frames = 1000, interval = 20)
plt.show()