import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

alfa = 2.4
L = 50
T_ext = 0
T_int = 670

N = 100
dx = L / ( N - 1 )
dt = 0.01
rtar = alfa * dt / dx ** 2

Nt = 900
tol = 1e-4

T = np.zeros((N,N))
T_save = {0 : T.copy()}

fig, ax = plt.subplots()

#im = ax.imshow(
 #   T.T,
  #  origin = 'lower',
   # extent = [0, L, 0, L],
    #cmap = 'viridis',
    #vmin = -0.5,
    #vmax = 1.0
    #)
im = ax.imshow(T, animated = True,
               origin = 'lower',
    extent = [0, L, 0, L],
    cmap = 'coolwarm',
    vmin = 0,
    vmax = T_int)
plt.colorbar(im, ax = ax)
def animate(frame):
    global T
    T[0,:] = T_ext
    T[-1,:] = T_ext
    T[:, 0] = T_ext
    T[:, -1] = T_ext
    T[45:55, 45:55] = T_int
    T_new = T.copy()
    T_new[1:-1, 1:-1] = T[1:-1, 1:-1] + rtar * (T[2:, 1:-1] + T[:-2, 1:-1] + T[1:-1, 2:] + T[1:-1, :-2] - 4 * T[1:-1, 1:-1])
    T = T_new
    im.set_array(T)

    return [im]

anim = FuncAnimation(fig, animate, frames = Nt, interval = 30)
plt.show()