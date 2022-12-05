import openterrace
<<<<<<< HEAD:openterrace/tutorials/example2.py
import numpy as np

ot = openterrace.Simulate(t_end=3600*2, dt=0.05, n_bed=50)

Ri = 0.0585
Ro = 0.0716
T_init = 40+273.15
T_room = 80+273.15
h = 50

ot.bed.select_substance('ATS58')
ot.bed.select_domain_shape(domain='hollow_sphere_1d', Rinner=Ri, Router=Ro)
ot.bed.select_schemes(diff='central_difference_1d')
ot.bed.select_initial_conditions(T=T_init)
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), 0))
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))

ot.bed.select_source_term(source_type='thermal_resistance', R=1/(h*4*np.pi*Ro**2), T_inf=T_room, position=(slice(None, None, None), -1))

=======

ot = openterrace.Simulate(t_end=3600*4, dt=0.1, n_fluid=100, n_bed=10)

ot.fluid.select_substance(substance='water')
ot.fluid.select_domain_shape(domain='cylinder_1d', D=0.5, H=1)
ot.fluid.select_porosity(phi=0.4)
ot.fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
ot.fluid.select_initial_conditions(T=273.15+40, mdot=0.1)
ot.fluid.select_bc(bc_type='dirichlet', parameter='T', position=(slice(None, None, None), 0), value=273.15+80)
ot.fluid.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))

ot.bed.select_substance('ATS58')
ot.bed.select_domain_shape(domain='hollow_sphere_1d', Rinner=0.005, Router=0.02)
ot.bed.select_schemes(diff='central_difference_1d')
ot.bed.select_initial_conditions(T=273.15+40)
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), 0))
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))

ot.select_coupling(h_coeff='constant', h_value=50)
>>>>>>> development:tutorials/example2.py
ot.output_animation(save_int=500, animate_data_flag=True)
ot.run_simulation()