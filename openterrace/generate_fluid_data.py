import numpy as np
import matplotlib.pyplot as plt
import CoolProp.CoolProp as CP

fluid = 'Air'

x = np.arange(200,1000,10)
V = CP.PropsSI('V','P',101325,'T',x,fluid)
C = CP.PropsSI('C','P',101325,'T',x,fluid)
L = CP.PropsSI('L','P',101325,'T',x,fluid)

y = C*V/L

# calculate polynomial
z = np.polyfit(x, y, 3)
f = np.poly1d(z)

# calculate new x's and y's
x_new = np.linspace(x[0], x[-1], 50)
y_new = f(x_new)

# print coefficients
print('coefficients:', z)

# plot data and fit
plt.plot(x,y,'o', x_new, y_new)
plt.xlim([x[0]-1, x[-1] + 1 ])
plt.show()

