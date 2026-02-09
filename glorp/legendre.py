import numpy as np
import argparse
import sympy as sp

#definir argumentos
def parse_arguments():
    parser = argparse.ArgumentParser(description="Generador de los Polinomios de Legendre y sus polinomios asociados.")
    parser.add_argument("--pol", type=int, nargs=2, help='Introducir el polinomio junto a su número y grado.')
    #parser.add_argument("--l", type=int, help='Introducir el número del polinomio.')
    return  parser.parse_args()

def main():
    args = parse_arguments()
    #definir las variables junto a las ecuaciones a usar
    x = sp.Symbol('cos(x)')
    l = sp.Symbol('l',integer=True,nonnegative=True)
    m = sp.Symbol('m',integer=True,nonnegative=True)
    l, m = args.pol
    p_l = (1/((2**l)*sp.factorial(l)))*(sp.diff((x**2 - 1)**l,x,l))
    p_lm = ((-1)**(m))*((1-x**2)**(m/2))*(sp.diff(p_l,x,m))

    #imprimir el latex de los polinomios
    #print("El polinomio ", l,"-ésimo es: ",p_l)
    #print("Su polinomio asociado ",m,"-ésimo es: ",p_lm)
    pllatex = sp.latex(p_l)
    plmlatex = sp.latex(p_lm)
    print("wawa: ", pllatex)
    print("wawa: ", plmlatex)
if __name__ == "__main__":
    main()

