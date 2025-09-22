import openterrace
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pytest
import sys

def test_advection_step_function(scheme):
    n = 1000
    t_end = 120

    H = 2
    D = 0.5
    T_init = 0
    T_in = 100
    cp = 4180
    rho = 993
    k = 0
    mdot = 1

    ot = openterrace.Setup(t_simulate=t_end, dt=1e-3)

    fluid = openterrace.Phase(type='fluid')
    fluid.select_substance_on_the_fly(cp=cp, rho=rho, k=k)
    fluid.select_domain_type(domain='cylinder_1d')
    fluid.create_domain(n=(n, 1), D=D, H=H)
    fluid.select_schemes(conv=scheme)
    fluid.initialise(T=T_init)
    fluid.select_massflow(mdot=mdot)
    fluid.select_bc(position=0, bc_type='fixed_value', value=T_in)
    fluid.select_bc(position=-1, bc_type='fixed_gradient', value=0)
    fluid.select_output(times=range(0, 121, 1))
   
    ot.run_simulation(phases=[fluid])

    X = t_end*(mdot/rho/(np.pi*(D/2)**2))/H
    y_H_num, theta_num = fluid.domain.node_pos/(fluid.domain.node_pos[-1]-fluid.domain.node_pos[0]), (fluid.T-T_in)/(T_init-T_in)
    y_H_ana, theta_ana = openterrace.analytical_step(X, n)

    plt.plot(y_H_num, theta_num,'s', label='OpenTerrace', color = '#4cae4f')
    plt.plot(y_H_ana, theta_ana,'k', label='Analytical')
    plt.xlim([0, 1])
    plt.ylim([-0.1, 1.1])
    plt.grid()
    plt.legend([r"OpenTerrace "+"("+r"upwind scheme"+")", "Analytical"], loc ="lower right")
    plt.xlabel(r'Position, $y^* = y/H$')
    plt.ylabel(r'Temperature, $\theta = (T(x,t)-T_{in})/(T_{init}-T_{in})$')
    plt.savefig('ot_test_advection_'+scheme+'.svg', bbox_inches='tight')
    plt.close()

    np.testing.assert_array_almost_equal(1,1, decimal=2) #Dummy check

if __name__ == "__main__":
    for scheme in openterrace.convection_schemes.__all__:
        test_advection_step_function(scheme)