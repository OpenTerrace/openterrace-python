""" This example shows how to simulate a cylindrical thermal storage tank with air and spherical magnetite stones as the bed material. """

import openterrace

ot = openterrace.Simulate(t_end=3600*6, dt=0.025, n_fluid=50, n_bed=5)

ot.fluid.select_substance(substance='air')
ot.fluid.select_domain_shape(domain='cylinder_1d', D=0.5, H=2)
ot.fluid.select_porosity(phi=0.4)
ot.fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
ot.fluid.select_initial_conditions(T=273.15+50, mdot=0.1)
ot.fluid.select_bc(bc_type='dirichlet', parameter='T', position=(slice(None, None, None), 0), value=273.15+600)
ot.fluid.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))

ot.bed.select_substance('magnetite')
ot.bed.select_domain_shape(domain='sphere_1d', R=0.01)
ot.bed.select_schemes(diff='central_difference_1d')
ot.bed.select_initial_conditions(T=273.15+50)
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), 0))
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))

ot.select_coupling(h_coeff='constant', h_value=20)
ot.output_animation(save_int=6000)
ot.run_simulation()