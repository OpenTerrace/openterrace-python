""" This example shows how to simulate heat diffusion in a hollow sphere made out of ATS58 (PCM material). """

import openterrace

Ri = 0.005
Ro = 0.025
T_init = 40+273.15
T_room = 80+273.15
h = 50

ot = openterrace.Simulate(t_end=7200, dt=0.05, sim_name='tutorial3')

bed = ot.createPhase(n=30, type='bed')
bed.select_substance(substance='ATS58')
bed.select_domain_shape(domain='hollow_sphere_1d', Rinner=Ri, Router=Ro)
bed.select_schemes(diff='central_difference_1d')
bed.select_initial_conditions(T=T_init)
bed.select_bc(bc_type='zeroGradient', parameter='T', position=(slice(None, None, None), 0))
bed.select_bc(bc_type='zeroGradient', parameter='T', position=(slice(None, None, None), -1))
bed.select_source_term(source_type='thermal_resistance', R=1/(h*4*3.14159*Ro**2), T_inf=T_room, position=(slice(None, None, None), -1))
bed.select_output(times=range(0, 7200, 300), parameters=['T'])

ot.run_simulation()
ot.generate_plots()
ot.generate_animations()