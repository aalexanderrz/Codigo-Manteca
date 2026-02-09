import numpy as np
import sympy as smp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#Define our function and variables

#def derivative(func):
 #   x = smp.symbols('x')
  #  return smp.diff(func)

initial_guess = 100
max_iterations = 100
time = 5e3
tolerance = 1e-7
x = smp.symbols('x')
func = smp.cos(x/10)*(x**2)
func_prime = smp.diff(func)
ffunc = smp.lambdify(x,func)
dffunc = smp.lambdify(x,func_prime)

#make the array that will house our guesses
guesses = []
#Find the guesses along with our stimation for the root and give it to the viewer
def newton(ini, tol, max):
    current_guess = initial_guess
    for iteration in range(max):
        f_value = ffunc(current_guess)
        f_prime_value = dffunc(current_guess)
        guesses.append(current_guess)
        if f_prime_value == 0:
            raise ValueError("Derivative is zero. No solution found.")
        next_guess = current_guess - f_value / f_prime_value
        if abs(next_guess - current_guess) < tolerance:
            return next_guess, iteration + 1
        current_guess = next_guess
        
root, iterations = newton(initial_guess,tolerance, max_iterations)
print(f"Root found: {root} in {iterations} iterations")
#Prepare the plots for the animation

def line(x0,y0,dfunc):
    x = np.linspace(guesses[0]-guesses[-1]/3,guesses[-1]+guesses[-1]/3,1000)
    y = dfunc*(x-x0)+y0
    return y

intv = time/iterations

x = np.linspace(guesses[0]-guesses[-1]/3,guesses[-1]+guesses[-1]/3,1000)
yf = ffunc(x)
fig, axis = plt.subplots()
axis.plot(x,yf)
axis.set_xlim([guesses[0]-guesses[-1]/3,guesses[-1]+guesses[-1]/3])
axis.set_ylim(min(ffunc(x))-2,max(ffunc(x)+2))
axis.grid()
axis.axhline(0, color='black', linewidth=.5)
axis.axvline(0, color='black', linewidth=.5)

textstr = '\n'.join((
    f'Initial guess: {initial_guess:.2f}',
    f'Iterations: {iterations:.2f}',
    f'Root found: {root:.2f}'))

fig.text(0.70, 0.81, textstr, transform=axis.transAxes, bbox=dict(facecolor='white', edgecolor='black'))


animated_plot, = axis.plot([],[])
animated_dot, = axis.plot([],[],'o', markersize = 10)


def update_data(frames):
    animated_plot.set_data(x,line(guesses[frames],ffunc(guesses[frames]),dffunc(guesses[frames])))
    animated_dot.set_data([guesses[frames]],[ffunc(guesses[frames])])

animation = FuncAnimation(fig=fig,
                          func=update_data,
                          frames=iterations,
                          interval=int(intv)
                        )
#animation.save("root_traviesa.gif")
plt.show()
