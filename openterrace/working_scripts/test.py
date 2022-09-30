import numpy as np
import time

def fcn(x):
    return 3*x**2+17*x**1+1


x = 5

t0 = time.time()
for i in range(10000):
    fcn(x*i)
print(time.time()-t0)

t0 = time.time()
for i in range(10000):
    np.polyval([3,17,1], x*i)
print(time.time()-t0)