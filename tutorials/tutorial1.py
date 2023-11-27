""" This example shows how to simulate advection of temperature in a cylindrical tank without any bed material. """

import openterrace

ot = openterrace.Simulate(t_end=60*10, dt=0.01, sim_name='tutorial1')

ot.fluid = ot.Phase(n=500, type='fluid')
ot.fluid.select_substance_on_the_fly(rho=1000, cp=4200, k=0.6)
ot.fluid.select_domain_shape(domain='cylinder_1d', D=0.3, H=1)
ot.fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
ot.fluid.select_initial_conditions(T=273.15+100, mdot=0.1)
ot.fluid.select_bc(bc_type='fixedValue', parameter='T', position=(slice(None, None, None), 0), value=273.15+600)
ot.fluid.select_bc(bc_type='zeroGradient', parameter='T', position=(slice(None, None, None), -1), value=0)
ot.fluid.select_output(times=range(0, 10*60+60, 60), parameters=['T'])

ot.run_simulation()
ot.generate_plots()
ot.generate_animations()