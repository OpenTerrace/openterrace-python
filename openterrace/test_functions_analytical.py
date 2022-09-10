import numpy as np
from scipy.optimize import brentq

def theta_fcn(Bi=None, Fo=None, r_r0=None, n_terms=10):
    def lambda_fcn(Bi, i):
        left = np.pi*(i) + 1e-12
        right = np.pi*(i+1) - 1e-12
        return brentq(lambda x: 1-x/np.tan(x)-Bi, left, right)

    theta = 0
    for i in range(0,n_terms):
        lambda_i = lambda_fcn(Bi,i)
        print(np.isclose(1-lambda_i/np.tan(lambda_i), Bi))
        if r_r0 == 0:
            theta += 4*(np.sin(lambda_i)-lambda_i*np.cos(lambda_i)) / (2*lambda_i - np.sin(2*lambda_i)) * np.exp(-lambda_i**2*Fo)
        else:
            theta += 4*(np.sin(lambda_i)-lambda_i*np.cos(lambda_i)) / (2*lambda_i - np.sin(2*lambda_i)) * np.exp(-lambda_i**2*Fo) * np.sin(lambda_i*r_r0)/(lambda_i*r_r0)
    return theta

Bi = 1200*0.025/0.627
Fo = 0.209
r_r0 = 0

theta = theta_fcn(Bi, Fo, r_r0)
print(theta)