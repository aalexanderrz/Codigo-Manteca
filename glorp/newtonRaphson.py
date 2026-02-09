import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols
from sympy import sympify
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Newton-Raphson Method")
    parser.add_argument("--function", type=str, help="Function in terms of x")
    parser.add_argument("--initial_guess", type=float, help="Initial guess for the root")
    parser.add_argument("--tolerance", type=float, default=1e-7, help="Tolerance for convergence")
    parser.add_argument("--max_iterations", type=int, default=100, help="Maximum number of iterations")
    parser.add_argument("--plot", action='store_true', help="Plot the function and its derivative")
    return parser.parse_args()

def plot_function(func, func_prime, x_range):
    x_vals = np.linspace(x_range[0], x_range[1], 100)
    y_vals = [float(func.subs(symbols('x'), val)) for val in x_vals]
    y_vals_prime = [float(func_prime.subs(symbols('x'), val)) for val in x_vals]
    
    plt.plot(x_vals, y_vals)
    plt.plot(x_vals, y_vals_prime)
    plt.axhline(0, color='black', lw=0.5, ls='--')
    plt.title('Function Plot and its Derivative')
    plt.xlabel('x')
    plt.ylabel('f(x) and f\'(x)')
    plt.grid()
    plt.show()

def derivative(func):
    x = symbols('x')
    return func.diff(x)

def newton_raphson(func, func_prime, initial_guess, tolerance, max_iterations):
    current_guess = initial_guess

    for iteration in range(max_iterations):
        f_value = func.subs(symbols('x'), current_guess).evalf()
        f_prime_value = func_prime.subs(symbols('x'), current_guess).evalf()
        
        if f_prime_value == 0:
            raise ValueError("Derivative is zero. No solution found.")
        
        next_guess = current_guess - f_value / f_prime_value
        
        if abs(next_guess - current_guess) < tolerance:
            return next_guess, iteration + 1
        
        current_guess = next_guess
    
    raise ValueError("Maximum iterations reached. No solution found.")

def main():
    args = parse_arguments()
    
    x = symbols('x')
    func = sympify(args.function)
    func_prime = derivative(func)

    if args.plot:
        plot_function(func, func_prime, (args.initial_guess - 10, args.initial_guess + 10))
    else:
        try:
            root, iterations = newton_raphson(func, func_prime, args.initial_guess, args.tolerance, args.max_iterations)
            print(f"Root found: {root} in {iterations} iterations")
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()

