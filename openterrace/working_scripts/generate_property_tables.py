import numpy as np
import matplotlib.pyplot as plt
import CoolProp.CoolProp as CP

fluid = 'Water'

T = np.arange(273.2,373.15,1)

H = CP.PropsSI('H','P',101325,'T',T,fluid)
D = CP.PropsSI('D','P',101325,'H',H,fluid)
L = CP.PropsSI('L','P',101325,'H',H,fluid)
C = CP.PropsSI('C','P',101325,'H',H,fluid)
V = CP.PropsSI('V','P',101325,'H',H,fluid)
Pr = C*V/L

par = C

# calculate polynomial
z = np.polyfit(H, par, 4)
f = np.poly1d(z)

# # calculate new x's and y's
H_new = np.linspace(H[0], H[-1], 50)
par_new = f(H_new)

print(f)
print(z)
# plot data and fit
plt.plot(H, par, '-k', H_new, par_new, '-ok')
plt.show()
