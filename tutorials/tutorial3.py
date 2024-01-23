""" This example shows how to simulate heat diffusion in a sphere made out of swedish diabase stone. """

import openterrace

R = 0.025
T_init = 40+273.15
T_room = 80+273.15
h = 200

ot = openterrace.Simulate(t_end=15*60, dt=0.01, sim_name='tutorial3')

bed = ot.createPhase(n=50, type='bed')
bed.select_substance('swedish_diabase')
bed.select_domain_shape(domain='sphere_1d', R=R)
bed.select_schemes(diff='central_difference_1d')
bed.select_initial_conditions(T=T_init)
bed.select_bc(bc_type='zeroGradient', parameter='T', position=(slice(None, None, None), 0))
bed.select_bc(bc_type='zeroGradient', parameter='T', position=(slice(None, None, None), -1))
bed.select_source_term(source_type='thermal_resistance', R=1/(h*4*3.14159*R**2), T_inf=T_room, position=(slice(None, None, None), -1))
bed.select_output(times=range(0, 15*60+60, 60))

ot.run_simulation()
ot.generate_plot(x=bed.node_pos, y=bed.data.T, times=bed.data.time, xlabel='Position', ylabel='Temperature')
ot.generate_animation(x=bed.node_pos, y=bed.data.T, times=bed.data.time, xlabel='Position', ylabel='Temperature')