import openterrace
import numpy as np

ot = openterrace.GlobalParameters(t_end=3600*2, dt=0.05, n_bed=50)

Rinner = 0.0585
Router = 0.0716
T_init = 40+273.15
T_room = 80+273.15
h = 50

ot.bed.select_substance('ATS58')
ot.bed.select_domain_shape(domain='hollow_sphere_1d', Rinner=Rinner, Router=Router)
ot.bed.select_schemes(diff='central_difference_1d')
ot.bed.select_initial_conditions(T=T_init)
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), 0))
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))

ot.bed.select_source_term(source_type='thermal_resistance', R=1/(h*4*np.pi*Router**2), T_inf=T_room, position=(slice(None, None, None), -1))

ot.animate(save_int=500, animate_data_flag=True)
ot.run_simulation()