import matplotlib.pyplot as plt
import numpy as np
from sympy import var
from sympy import sympify

while True:
    try:
        desde = float(input('Desde: '))
        hasta = float(input('Hasta: '))
        if desde >= hasta:
            print("El valor 'desde' debe ser menor que 'hasta'")
            continue
        break
    except ValueError:
        print('Entrada inválidad. Por favor ingresar números válidos')


x = var('x')
user_input = input("Ingrese la función en términos de x: ")
function = sympify(user_input)
y = [float(function.subs(x,val)) for val in np.linspace(desde,hasta,100)]
x = np.linspace(desde, hasta, 100)

plt.plot(x,y)
plt.show()