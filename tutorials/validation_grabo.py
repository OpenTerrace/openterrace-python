""" This example shows how to simulate advection of temperature in a cylindrical tank without any bed material. """

import openterrace
import numpy as np
import matplotlib.pyplot as plt

ot = openterrace.Simulate(t_end=600*60, dt=0.1, sim_name='validation_grabo')

fluid = ot.createPhase(n=290, type='fluid')
fluid.select_substance_on_the_fly(rho=1000, cp=4200, k=0.6)
fluid.select_domain_shape(domain='block_1d', A=0.734**2, L=1.45)
#fluid.select_domain_shape(domain='cylinder_1d', D=0.79, H=1.9)
fluid.select_porosity(phi=0.65)
fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
fluid.select_initial_conditions(T=273.15+47)
fluid.select_massflow(mdot=360/3600) #ok
fluid.select_bc(bc_type='fixedValue', parameter='T', position=(slice(None, None, None), 0), value=273.15+67)
fluid.select_bc(bc_type='zeroGradient', parameter='T', position=(slice(None, None, None), -1), value=0)
fluid.select_output(times=range(0, 600*60+60, 30))

bed = ot.createPhase(n=40, n_other=290, type='bed')
bed.select_substance('ATS58')
bed.select_domain_shape(domain='hollow_sphere_1d', Rinner=0.0553, Router=0.0665)
bed.select_schemes(diff='central_difference_1d')
bed.select_initial_conditions(T=273.15+47)
bed.select_bc(bc_type='zeroGradient', parameter='T', position=(slice(None, None, None), 0))
bed.select_bc(bc_type='zeroGradient', parameter='T', position=(slice(None, None, None), -1))
bed.select_output(times=range(0, 600*60+60, 30))

ot.select_coupling(fluid_phase=0, bed_phase=1, h_exp='constant', h_value=100)
ot.run_simulation()

plt.plot(fluid.data.time/60,fluid.data.T[:,0,-1]-273.15)
plt.show()
plt.grid()
plt.xlabel('Time (min)')
plt.ylabel('Outlet temperature (C)')
plt.xlim([0, 900])
plt.ylim([45, 70])
plt.savefig('out.png')

