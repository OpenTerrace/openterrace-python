import numpy as np
import matplotlib.pyplot as plt
import CoolProp.CoolProp as CP

fluid = 'Water'


T1 = CP.PropsSI('T','P',101325,'Q',0,fluid)
T2 = CP.PropsSI('T','P',101325,'Q',1,fluid)
print(T1,T2)

T = np.arange(200, 1000, 10)
V = CP.PropsSI('V','P',101325,'T',T,fluid)
C = CP.PropsSI('C','P',101325,'T',T,fluid)
L = CP.PropsSI('L','P',101325,'T',T,fluid)
H = CP.PropsSI('H','P',101325,'T',T,fluid)

# plot data and fit
plt.plot(H, T, '-ok')
plt.show()

# calculate polynomial
z = np.polyfit(H, T, 2)
f = np.poly1d(z)

# # calculate new x's and y's
# H_new = np.linspace(H[0], H[-1], 50)
# T_new = f(H_new)

# # print coefficients
# print('coefficients:', z)

