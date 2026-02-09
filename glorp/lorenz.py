import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation
#Lorenz's parameters (chaotic)
sigma = 10
beta = 8/3
rho = 28

def rk4singlestep(fun, dt, t0, q0):
    # Generic diff eq: \dot{q} = f(t,q), q can be a vector for 2D or 3D cases.
    f1 = fun(t0,q0)
    f2 = fun(t0 + dt/2, q0 + (dt/2)*f1)
    f3 = fun(t0 + dt/2, q0 + (dt/2)*f2)
    f4 = fun(t0 + dt, q0 + dt*f3)
    qout = q0 + (dt/6)*(f1+2*f2+2*f3+f4) 
    return qout

def lorenz(t, state):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return np.array([dxdt, dydt, dzdt])

# Initial conditions
x0 = 5.0 #-8
y0 = 1.0 #8
z0 = 1.0 #27
initial_state = np.array([x0, y0, z0])

# Compute the trajectory using RK4
t0 = 0.0
tf = 50.0 #10.0
dt = 0.1
num_steps = int((tf - t0) / dt)
trajectory_rk4 = np.zeros((num_steps, 3))
trajectory_rk4[0] = initial_state
for i in range(1, num_steps):
    trajectory_rk4[i] = rk4singlestep(lorenz, dt, t0 + (i-1)*dt, trajectory_rk4[i-1])

# Compute the trajectory using solve_ivp
sol = solve_ivp(lorenz, [t0, tf], initial_state, t_eval=np.linspace(t0, tf, num_steps))
trajectory_scipy = sol.y.T

# 3D vector field (direction field) grid
#xmin, xmax = -20, 20
#ymin, ymax = -30, 30
#zmin, zmax = 0, 50
#grid_n = 10
#X, Y, Z = np.meshgrid(
   # np.linspace(xmin, xmax, grid_n),
  #  np.linspace(ymin, ymax, grid_n),
  #  np.linspace(zmin, zmax, grid_n)
#)
#U = sigma * (Y - X)
#V = X * (rho - Z) - Y
#W = X * Y - beta * Z
#N = np.sqrt(U**2 + V**2 + W**2)
#N[N == 0] = 1.0
#U, V, W = U / N, V / N, W / N

# Plotting the results (trajectories)
fig, ax = plt.subplots(subplot_kw={'projection':'3d'})   

RK4, = ax.plot(trajectory_rk4[:, 0], trajectory_rk4[:, 1], trajectory_rk4[:, 2], color='blue', label='rk4')
ax.set_title('Lorenz Attractor - RK4 Method vs Scipy')
wA, = ax.plot(trajectory_scipy[:, 0], trajectory_scipy[:, 1], trajectory_scipy[:, 2], color='red',label='Scipy')

def animate(frame):
    RK4.set_data(trajectory_rk4[:10*frame, 0], trajectory_rk4[:10*frame, 1])
    RK4.set_3d_properties(trajectory_rk4[:10*frame, 2])
    wA.set_data(trajectory_scipy[:10*frame, 0], trajectory_scipy[:10*frame, 1])
    wA.set_3d_properties(trajectory_scipy[:10*frame, 2])
    return RK4, wA

tiempo = 5e3

animation = FuncAnimation(fig=fig,func=animate,frames=500,interval=1)

try:
    animation.save('animation.gif',writer='pillow',fps=30)
except ValueError as e:
    print("No se pudo guardar {e}.")
plt.show()