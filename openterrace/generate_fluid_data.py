import numpy as np
import matplotlib.pyplot as plt
import CoolProp.CoolProp as CP

fluid = 'Air'

T = np.arange(200,1000,10)
V = CP.PropsSI('V','P',101325,'T',T,fluid)
C = CP.PropsSI('C','P',101325,'T',T,fluid)
L = CP.PropsSI('L','P',101325,'T',T,fluid)
H = CP.PropsSI('H','P',101325,'T',T,fluid)

# calculate polynomial
z = np.polyfit(H, T, 2)
f = np.poly1d(z)

# calculate new x's and y's
H_new = np.linspace(H[0], H[-1], 50)
T_new = f(H_new)

# print coefficients
print('coefficients:', z)

# plot data and fit
plt.plot(H,T,'o', H_new, T_new)
#plt.xlim([x[0]-1, x[-1] + 1 ])
plt.show()

