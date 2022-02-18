import pyromat as pm
import numpy as np
import matplotlib.pyplot as plt

T = np.linspace(300.,1000.,101)
air = pm.get('mp.air')
plt.plot(T, air.cp(T))
plt.show()