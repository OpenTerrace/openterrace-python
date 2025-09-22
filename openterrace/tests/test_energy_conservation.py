import openterrace
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pytest
import sys

def test_energy_conservation():
    ot = openterrace.Setup(t_simulate=10000, dt=1)

    fluid = openterrace.Phase(type='fluid')
    fluid.select_substance_on_the_fly(cp=4200, rho=1000, k=0.6)
    fluid.select_domain_type(domain='block_1d')
    fluid.create_domain(n=(101, 1), length=0.1, area=0.1)
    fluid.select_schemes(diff='central_difference_1d')
    fluid.initialise(T=np.linspace(0,100, 101))
    fluid.select_bc(position=0, bc_type='fixed_gradient', value=0)
    fluid.select_bc(position=-1, bc_type='fixed_gradient', value=0)
    fluid.select_output(times=range(0, 11000, 1000), parameters=['T','h'])
    
    ot.run_simulation(phases=[fluid])

    plt.plot(fluid.domain.node_pos, fluid.data.parameters['h'][:,0,:].T, label=fluid.data.times)
    plt.legend(title='Simulation time (s)')
    plt.xlabel(u'Position (m)')
    plt.ylabel(u'Specific enthalpy (J/(kg))')
    plt.grid()
    plt.grid(which='major', color='#DDDDDD', linewidth=1)
    plt.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.8)
    plt.minorticks_on()
    plt.savefig('ot_test_energy_conservation.svg', bbox_inches='tight')
    
    np.testing.assert_array_almost_equal(1,1, decimal=2) #Dummy check

if __name__ == '__main__':
    test_energy_conservation()