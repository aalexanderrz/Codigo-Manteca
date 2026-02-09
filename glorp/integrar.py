import numpy as np
import sympy as sp
import argparse 

def parse_arguments():
    parser = argparse.ArgumentParser(description="Simphson method of integration")
    parser.add_argument("--function", type=str, help="Function in terms of x.")
    parser.add_argument("--interval", type=float, nargs = 2, help="Interval to integrate over.")
    parser.add_argument("--n", type=int, help="Number of partitions for the interval")
    return parser.parse_args()

def error(f,a,b,h):
    df = sp.diff(f,sp.Symbol('x'),4)
    M = f.subs(sp.Symbol('x'),b).evalf()
    return (h**4)*(b-a)*M/180

def simpson(f,a,b,n):
    h = (b-a)/n
    S = 0
    for i in range(n+1):
        if i == 0:
            S = S + f.subs(sp.Symbol('x'),a+h*i).evalf()
        else:
            if i == n:
                S = S + f.subs(sp.Symbol('x'),a+h*i).evalf()   
            else: 
                if i % 2 == 0:
                    S = S + 2*f.subs(sp.Symbol('x'),a+h*i).evalf()    
                else:
                    S = S + 4*f.subs(sp.Symbol('x'),a+h*i).evalf()               
    return [h*S/3,error(f,a,b,h)]


def main():
    args = parse_arguments()
    func = sp.sympify(args.function)
   
    n = args.n
    a, b = args.interval
    S_n = simpson(func,a,b,n)
    print('La integral para ',args.function,'en el intervalo [',a,',',b,'] es: ',S_n[0],'. Con un error de: ',S_n[1])
if __name__ == "__main__":
    main()
