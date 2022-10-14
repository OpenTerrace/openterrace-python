import pytest
import numpy as np
from scipy.optimize import brentq

def test_sphere():
    def theta_fcn(Bi=None, Fo=None, r_r0=None, n_terms=5):
        def lambda_fcn(Bi, i):
            left = np.pi*(i) + 1e-12
            right = np.pi*(i+1) - 1e-12
            return brentq(lambda x: 1-x/np.tan(x)-Bi, left, right)

        theta = 0
        for i in range(0,n_terms):
            lambda_i = lambda_fcn(Bi,i)
            if not np.isclose(1-lambda_i/np.tan(lambda_i), Bi):
                raise Exception("root of lambda function not found.")
            if r_r0 == 0:
                theta += 4*(np.sin(lambda_i)-lambda_i*np.cos(lambda_i)) / (2*lambda_i - np.sin(2*lambda_i)) * np.exp(-lambda_i**2*Fo)
            else:
                theta += 4*(np.sin(lambda_i)-lambda_i*np.cos(lambda_i)) / (2*lambda_i - np.sin(2*lambda_i)) * np.exp(-lambda_i**2*Fo) * np.sin(lambda_i*r_r0)/(lambda_i*r_r0)
        return theta

    h = 1200
    Lc = 0.025
    k = 0.627
    Bi = h*Lc/k
    Fo = 0.2085
    r_r0 = 0

    theta = theta_fcn(Bi, Fo, r_r0)
    Ti = 5
    Tinf = 95
    T = theta*(Ti-Tinf)+Tinf
    print(theta, T)
    assert 1 == 1