""" This example sets up a water tank with PCM material as the bed material. """

import openterrace

ot = openterrace.Simulate(t_end=7200, dt=0.05)

ot.fluid = ot.Phase(n=100, type='fluid')
ot.fluid.select_substance(substance='water')
ot.fluid.select_domain_shape(domain='cylinder_1d', D=0.1, H=1)
ot.fluid.select_porosity(phi=0.4)
ot.fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
ot.fluid.select_initial_conditions(T=273.15+40, mdot=0.01)
ot.fluid.select_bc(bc_type='dirichlet', parameter='T', position=(slice(None, None, None), 0), value=273.15+80)
ot.fluid.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))
ot.fluid.select_output(times=range(0, 7200+60, 60), parameters=['T'])

ot.bed = ot.Phase(n=10, n_other=100, type='bed')
ot.bed.select_substance('ATS58')
ot.bed.select_domain_shape(domain='hollow_sphere_1d', Rinner=0.005, Router=0.02)
ot.bed.select_schemes(diff='central_difference_1d')
ot.bed.select_initial_conditions(T=273.15+40)
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), 0))
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))
ot.bed.select_output(times=range(0, 7200+60, 900), parameters=['T'])

ot.select_coupling(h_coeff='constant', h_value=200)
ot.run_simulation()
ot.generate_plots()