#queremos --x [1,2,3,4,5] --y [1,2,3,4,5] --min --max --mean --std --regression m, b, error m, error b, r**2, --gauss
import argparse
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def parse_arguments():
    parser = argparse.ArgumentParser(description="EL Chepe Aquillion")
    parser.add_argument("--x", type=float, nargs='*', help='Introducir valores de x')
    parser.add_argument("--y", type=float, nargs='*', help='Introducir valores de y.')
    parser.add_argument("--lin", action='store_true', help = 'Realizar una regresión lineal para los datos.')
    parser.add_argument("--gauss", action='store_true', help = 'Realizar una regresión gaussiana para los datos.')
    parser.add_argument("--maxx", action='store_true', help = 'Encontrar el valor máximo de x.')
    parser.add_argument("--maxy", action='store_true', help = 'Encontrar el valor máximo de y.')
    parser.add_argument("--mean", action='store_true', help = 'Envontrar la media de los valores de y.')
    parser.add_argument("--std", action='store_true', help = 'Encontrar la desviación estándar de los valores de y.')
    return  parser.parse_args()

def min_num(nums):
    print("El valor mínimo es ", min(nums))

def max_num(nums):
    print("El valor máximo es ", max(nums))

def mean(nums):
    mean = sum(nums)/len(nums)
    print("La media es: ", mean)

def std(nums):
    mean = sum(nums)/len(nums)
    iterable = len(nums)-1
    count = 0
    for i in nums:
        count = (nums[i]-mean)**2 + count
    std = sqrt(count/(len(nums)-1))
    print("La desviación estándar es: ", std)

def lin(x,y):
    prod, x2, sumy, sumx, = 0, 0, 0, 0
    
    for i in range(len(x)):
        prod = x[i]*y[i] + prod
        x2, sumx ,sumy = x[i]**2 + x2, x[i] + sumx , y[i] + sumy
    m = (len(x)*prod-sumx*sumy)/(len(x)*x2-sumx**2)  
    b = (sumy*x2-sumx*prod)/(len(x)*x2-sumx**2)
    print("La regresión tiene los parámetros: m = ", m, " y b = ", b)
    wa = np.linspace(min(x)-1, max(x) +1, 100)
    reg = m*wa + b
    plt.scatter(x,y, color='red', label='Datos')
    plt.plot(wa, reg, '--', color='blue', label='Regresión lineal')
    plt.legend(loc='upper right', fontsize=10, ncol=1)
    plt.show()
         
def model(x,A,b,c):
        return A*np.exp(-(x-b)**2/c**2)

def gauss(x,y):
        maxx = max(x)
        maxy = max(y)
        minx = min(x)
        miny = min(y)
        meanx = sum(x)/len(x) 
        sigmoid = (maxy-miny)/4.70964
        popt, pcov = curve_fit(model,x,y,p0=[maxy,meanx,sigmoid])
        Amod, bmod, cmod = popt
        x_mod = np.linspace(-minx,maxx,1000)
        y_mod = Amod*np.exp(-(x_mod-bmod)**2/cmod**2)
        era, erb, erc = np.sqrt(np.diag(pcov))

        print(f"Los valores para el modelo A*e^(-(x-b)^2/c^2), son: A = {Amod:.4f} b = {bmod:.4f} y c = {cmod:.4f} con errores {era:.2f}, {erb:.2f} y {erc:.2f} respectivamente")

        textstr = '\n'.join((
        r'$\sigma_a=%.4f$' % (era),
        r'$\sigma_b=%.4f$' % (erb),
        r'$\sigma_c=%.4f$' % (erc)))

        fig, ax = plt.subplots()
        ax.scatter(x,y,label='Data')
        ax.plot(x_mod,y_mod, label='Model')
        fig.text(0.05, 0.81, textstr, transform=ax.transAxes, bbox=dict(facecolor='white', edgecolor='black'))
        ax.legend(loc='upper right')
        ax.set_title('Data')
        plt.show()
        
   
#at_the_club = 'straight up jorking it, and by it... let\'s just say: MY PEANUTS'

def main():
    args = parse_arguments()
    
    if args.maxx:
        min_num(args.y)
    elif args.maxy:
        max_num(args.y)
    elif args.mean:
        mean(args.y)
    elif args.std:
        std(args.y)   
    elif args.lin:
        lin(args.x,args.y)
    elif args.gauss:
        gauss(args.x,args.y) 
                    
if __name__ == "__main__":
    main()




