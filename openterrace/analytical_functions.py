import numpy as np
from scipy.optimize import brentq

def analytical_wall(Bi:float, Fo:float, n:int):
    def theta_fcn(Bi:float, Fo:float, r_r0:float, n_terms:int=100):
        def lambda_fcn(Bi, i):
            left = np.pi*i
            right = left + np.pi/2 - 1e-12
            return brentq(lambda x: x*np.tan(x)-Bi, left, right)

        theta = 0
        for i in range(0, n_terms):
            lambda_i = lambda_fcn(Bi,i)
            if not np.isclose(lambda_i*np.tan(lambda_i), Bi):
                raise Exception("root of lambda function not found.")
            if x_x0 == 0:
                theta += 4*np.sin(lambda_i)/(2*lambda_i+np.sin(2*lambda_i)) * np.exp(-lambda_i**2*Fo)
            else:
                theta += 4*np.sin(lambda_i)/(2*lambda_i+np.sin(2*lambda_i)) * np.exp(-lambda_i**2*Fo) * np.cos(lambda_i*x_x0)
        return theta

    theta_arr = []
    x_x0_arr = np.linspace(0,1,n)
    for x_x0 in x_x0_arr:
        theta = theta_fcn(Bi, Fo, x_x0)
        theta_arr.append(theta)
    return x_x0_arr, theta_arr

def analytical_sphere(Bi:float, Fo:float, n:int):
    def theta_fcn(Bi:float, Fo:float, r_r0:float, n_terms:int=100):
        def lambda_fcn(Bi, i):
            left = np.pi*(i) + 1e-12
            right = np.pi*(i+1) - 1e-12
            return brentq(lambda x: 1-x/np.tan(x)-Bi, left, right)

        theta = 0
        for i in range(0, n_terms):
            lambda_i = lambda_fcn(Bi,i)
            if not np.isclose(1-lambda_i/np.tan(lambda_i), Bi):
                raise Exception("root of lambda function not found.")
            if r_r0 == 0:
                theta += 4*(np.sin(lambda_i)-lambda_i*np.cos(lambda_i)) / (2*lambda_i - np.sin(2*lambda_i)) * np.exp(-lambda_i**2*Fo)
            else:
                theta += 4*(np.sin(lambda_i)-lambda_i*np.cos(lambda_i)) / (2*lambda_i - np.sin(2*lambda_i)) * np.exp(-lambda_i**2*Fo) * np.sin(lambda_i*r_r0)/(lambda_i*r_r0)
        return theta

    theta_arr = []
    r_r0_arr = np.linspace(0,1,n)
    for r_r0 in r_r0_arr:
        theta = theta_fcn(Bi, Fo, r_r0)
        theta_arr.append(theta)
    return r_r0_arr, theta_arr