""" This example shows how to simulate heat diffusion in a sphere made out of swedish diabase stone. """

import openterrace

R = 0.025
T_init = 40+273.15
T_room = 80+273.15
h = 200

ot = openterrace.Simulate(t_end=15*60, dt=0.01, sim_name='tutorial2')

ot.bed = ot.Phase(n=50, type='bed')
ot.bed.select_substance('swedish_diabase')
ot.bed.select_domain_shape(domain='sphere_1d', R=R)
ot.bed.select_schemes(diff='central_difference_1d')
ot.bed.select_initial_conditions(T=T_init)
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), 0))
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))
ot.bed.select_source_term(source_type='thermal_resistance', R=1/(h*4*3.14159*R**2), T_inf=T_room, position=(slice(None, None, None), -1))
ot.bed.select_output(times=range(0, 15*60+60, 60), parameters=['T'])

ot.run_simulation()
ot.generate_plots()