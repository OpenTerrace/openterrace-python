import numpy as np
import matplotlib.pyplot as plt
import CoolProp.CoolProp as CP

fluid = 'Air'

T = np.arange(273.2,1000,1)

H = CP.PropsSI('H','P',101325,'T',T,fluid)
D = CP.PropsSI('D','P',101325,'H',H,fluid) #density
L = CP.PropsSI('L','P',101325,'H',H,fluid) #thermal conductivity
C = CP.PropsSI('C','P',101325,'H',H,fluid) #specific heat
V = CP.PropsSI('V','P',101325,'H',H,fluid) #viscosity
Pr = C*V/L

n_coeffs = np.array([1,3,2,3,2])
coeffs = []
for i,par in enumerate([T, D, L, C, V]):
    # calculate polynomial
    z = np.polyfit(H, par, n_coeffs[i])
    f = np.poly1d(z)
    coeffs.append([f.coef])

    # # calculate new x's and y's
    H_new = np.linspace(H[0], H[-1], 50)
    par_new = f(H_new)

    # plot data and fit
    #plt.plot(H, par, '-k', H_new, par_new, '-ok')
    #plt.show()

a = 1/coeffs[0][0][0]
b = -coeffs[0][0][1]/coeffs[0][0][0]

print(a,b)
