from openterrace.openterrace import OpenTerrace
import pytest
import numpy as np
from scipy.optimize import brentq
import matplotlib.pyplot as plt
 
def test_sphere(Bi:float, Fo:float):
    def theta_fcn(Bi:float, Fo:float, r_r0:float, n_terms:int=20):
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

    theta_arr = []
    r_r0_arr = np.linspace(0,1,n)
    for r_r0 in r_r0_arr:
        theta = theta_fcn(Bi, Fo, r_r0)
        theta_arr.append(theta)
    return r_r0_arr, theta_arr

n = 50
t_end = 240
Lc = 0.025
T_init = 0
T_inf = 100
h = 100000
cp = 1130
rho = 5150
k = 1.9

ot = OpenTerrace(t_end=t_end, dt=1e-2, n_bed=n)
ot.bed.define_substance_on_the_fly(cp=cp, rho=rho, k=k)
ot.bed.select_domain(domain='1d_sphere', D=Lc*2)
ot.bed.select_schemes(diff='central_difference_1d')
ot.bed.initialise(T=T_init)
ot.bed.define_bc(bc_type='dirichlet', parameter='T', position=np.s_[:,-1], value=T_inf)
ot.bed.define_bc(bc_type='neumann', parameter='T', position=np.s_[:,0])
ot.run_simulation()

Bi = h*Lc/k
Fo = (k/(rho*cp))*t_end/Lc**2

r_r0_ana, theta_ana = test_sphere(Bi, Fo)
r_r0_num, theta_num = ot.bed.domain.node_pos/(ot.bed.domain.node_pos[-1]-ot.bed.domain.node_pos[0]), (ot.bed.T[0,:]-T_inf)/(T_init-T_inf)

plt.plot(r_r0_num, theta_num,'s', label='OpenTerrace', color = '#4cae4f')
plt.plot(r_r0_ana, theta_ana,'k', label='Analytical')
plt.xlim([0,1])
plt.ylim([-0.1,1.1])
plt.grid()
plt.legend([r"OpenTerrace ($Bi=\infty$, "+r"$Fo=$"+f"{Fo:.2e}", "Analytical"], loc ="lower left")
plt.xlabel(r'Radial position, $r^* = r/r_0$')
plt.ylabel(r'Temperature, $\theta = (T-T_\infty)/(T_{init}-T_\infty)$')
plt.savefig('docs/_figures/test_sphere_0.svg', bbox_inches='tight')
plt.show()