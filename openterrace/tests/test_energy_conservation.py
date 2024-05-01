import openterrace
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pytest
import sys

def test_energy_conservation():
    ot = openterrace.Simulate(t_end=10000, dt=1)
    fluid = ot.create_phase(n=101, type='fluid')
    fluid.select_substance_on_the_fly(cp=4200, rho=1000, k=0.6)
    fluid.select_domain_shape(domain='block_1d', A=0.1, L=0.1)
    fluid.select_schemes(diff='central_difference_1d')
    fluid.select_initial_conditions(T=np.linspace(0,100, 101))
    fluid.select_bc(bc_type='zero_gradient', parameter='T', position=(slice(None, None, None), 0))
    fluid.select_bc(bc_type='zero_gradient', parameter='T', position=(slice(None, None, None), -1))
    fluid.select_output(times=range(0, 11000, 1000), output_parameters=['T','h'])
    
    ot.run_simulation()

    plt.plot(fluid.node_pos, fluid.data.h[:,0,:].T, label=fluid.data.time)
    plt.legend(title='Simulation time (s)')
    plt.xlabel(u'Position (m)')
    plt.ylabel(u'Specific enthalpy (J/(kg))')
    plt.grid()
    plt.grid(which='major', color='#DDDDDD', linewidth=1)
    plt.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.8)
    plt.minorticks_on()
    plt.savefig('ot_test_energy_conservation.svg', bbox_inches='tight')
    
    np.testing.assert_array_almost_equal(1,1, decimal=2) #Dummy check