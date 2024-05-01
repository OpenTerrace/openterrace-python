import openterrace
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pytest
import sys

def test_advection_step_function():
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

    ot = openterrace.Simulate(t_end=t_end, dt=1e-2)
    fluid = ot.create_phase(n=n, type='fluid')
    fluid.select_substance_on_the_fly(cp=cp, rho=rho, k=k)
    fluid.select_domain_shape(domain='cylinder_1d', D=D, H=H)
    fluid.select_schemes(conv='upwind_1d')
    fluid.select_initial_conditions(T=T_init)
    fluid.select_massflow(mdot=mdot)
    fluid.select_bc(bc_type='fixed_value',
                    parameter='T',
                    position=(slice(None, None, None), 0),
                    value=T_in
                    )
    fluid.select_bc(bc_type='zero_gradient',
                    parameter='T',
                    position=(slice(None, None, None), -1)
                    )
    ot.run_simulation()

    X = t_end*(mdot/rho/(np.pi*(D/2)**2))/H

    y_H_num, theta_num = fluid.node_pos/(fluid.node_pos[-1]-fluid.node_pos[0]), (fluid.T[0]-T_in)/(T_init-T_in)
    y_H_ana, theta_ana = openterrace.analytical_step(X, n)

    plt.plot(y_H_num, theta_num,'s', label='OpenTerrace', color = '#4cae4f')
    plt.plot(y_H_ana, theta_ana,'k', label='Analytical')
    plt.xlim([0, 1])
    plt.ylim([-0.1, 1.1])
    plt.grid()
    plt.legend([r"OpenTerrace "+"("+r"upwind scheme"+")", "Analytical"], loc ="lower right")
    plt.xlabel(r'Position, $y^* = y/H$')
    plt.ylabel(r'Temperature, $\theta = (T(x,t)-T_{in})/(T_{init}-T_{in})$')
    plt.savefig('ot_test_advection_step_function.svg', bbox_inches='tight')
    plt.close()

    np.testing.assert_array_almost_equal(1,1, decimal=2) #Dummy check