import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

error = 0.5*np.random.rand(30)
x = np.linspace(-2,4,30)
y = 3*np.exp(-(x-1)**2/2**2)+error


def model(x,A,b,c):
    return A*np.exp(-(x-b)**2/c**2)



popt, pcov = curve_fit(model,x,y,p0=[3.5,0,2.5])
Amod, bmod, cmod = popt
x_mod = np.linspace(-2,4,100)
y_mod = Amod*np.exp(-(x_mod-bmod)**2/cmod**2)
era, erb, erc = np.sqrt(np.diag(pcov))

print(f"Los valores, para el modelo A*e^(-(x-b)^2/c^2), son: A = {Amod:.4f} b = {bmod:.4f} y c = {cmod:.4f} con errores {era:.2f}, {erb:.2f} y {erc:.2f} respectivamente")

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
