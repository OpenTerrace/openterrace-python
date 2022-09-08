import numpy as np
from scipy.optimize import brentq
import matplotlib.pyplot as plt
import sys

def theta(Bi=None, Fo=None, r_r0=None, n=5):
    def lambda_fcn(Bi, i):
        left = 0.0001#np.pi*i
        right = left + np.pi/2 - 1e-12
        return brentq(lambda x: 1-x*np.cos(x)/np.sin(x)-Bi, left, right)

    theta = 0
    for i in range(0,n):
        print(Bi,i)
        lambda_i = lambda_fcn(Bi,i)
        print(np.allclose(1-lambda_i*np.cos(lambda_i)/np.sin(lambda_i),Bi))

        sys.exit()
        print(lambda_i)

        sys.exit()
        print(lambda_i)
        value = 4*(np.sin(lambda_i)-lambda_i*np.cos(lambda_i)) / (2*lambda_i - np.sin(2*lambda_i)) * np.exp(-lambda_i**2*Fo) * np.sin(lambda_i*r_r0)/(lambda_i*r_r0)
        print(i, value)
    return theta

theta(Bi=47.8, Fo=0.209, r_r0=0.0001, n=1)

# import unittest

# class TestSum(unittest.TestCase):

#     def test_sum(self):
#         self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

#     def test_sum_tuple(self):
#         self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")

# if __name__ == '__main__':
#     unittest.main()

# class TestFunctions():

#     def sphere_1d_diffusion(self, t_end=None, h=None, r=None, k=None, rho=None, cp=None, n_terms=5):
#         def lambda(self, Bi, n):
#             """Finds the first n solutions to the equation 1-lambda_n*cos(lambda_n)/sin(lambda_n) = Bi"""

#             return