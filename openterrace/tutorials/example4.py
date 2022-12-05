import openterrace
import numpy as np

ot = openterrace.Simulate(t_end=5*60, dt=0.01, n_bed=50)

D = 0.02
T_init = 40+273.15
T_room = 80+273.15
h = 200

ot.bed.select_substance('swedish_diabase')
ot.bed.select_domain_shape(domain='sphere_1d', R=D/2)
ot.bed.select_schemes(diff='central_difference_1d')
ot.bed.select_initial_conditions(T=T_init)
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), 0))
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))
ot.bed.select_source_term(source_type='thermal_resistance', R=1/(h*4*np.pi*(D/2)**2), T_inf=T_room, position=(slice(None, None, None), -1))

ot.output_animation(save_int=200, animate_data_flag=True)
ot.run_simulation()