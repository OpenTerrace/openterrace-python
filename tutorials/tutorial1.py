""" This example shows how to simulate advection of temperature in a cylindrical tank without any bed material. """

import openterrace
import matplotlib.pyplot as plt

ot = openterrace.Simulate(t_end=600, dt=0.01, sim_name='tutorial1')

fluid = ot.createPhase(n=20, type='fluid')
fluid.select_substance_on_the_fly(rho=1000, cp=4200, k=0.6)
fluid.select_domain_shape(domain='cylinder_1d', D=0.3, H=1)
fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
fluid.select_initial_conditions(T=273.15+100)
fluid.select_massflow(mdot=0.1)
fluid.select_bc(bc_type='fixedValue', parameter='T', position=(slice(None, None, None), 0), value=273.15+600)
fluid.select_bc(bc_type='zeroGradient', parameter='T', position=(slice(None, None, None), -1), value=0)
fluid.select_output(times=range(0, 15*60+60, 60))

ot.run_simulation()
<<<<<<< Updated upstream
ot.generate_plot(x=fluid.node_pos, y=fluid.data.T, times=fluid.data.time, xlabel='Position', ylabel='Temperature', name='fig2')
ot.generate_animation(x=fluid.node_pos, y=fluid.data.T, times=fluid.data.time, xlabel='Position', ylabel='Temperature', name='ani2')
=======
ot.generate_plot(x=fluid.node_pos, y=fluid.data.T, times=fluid.data.time, xlabel='Position', ylabel='Temperature', name='fig1')
ot.generate_animation(x=fluid.node_pos, y=fluid.data.T, times=fluid.data.time, xlabel='Position', ylabel='Temperature', name='ani1')
>>>>>>> Stashed changes
