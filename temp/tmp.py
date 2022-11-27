import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

x = np.linspace(0,2*np.pi,100)
Bi = 7.974481658692185
y = x*np.tan(x)-Bi

left = np.pi*0
right = left + np.pi/2 - 1e-12

x0 = brentq(lambda x: x*np.tan(x)-Bi, left, right)

i = 0
print(Bi, i)
left = np.pi*i
right = left + np.pi/2 - 1e-12
print(left, right)
