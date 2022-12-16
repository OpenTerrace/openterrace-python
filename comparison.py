""" This example sets up a water tank with PCM material as the bed material. """

import openterrace
import numpy as np

ot = openterrace.Simulate(t_end=600, dt=0.0025, n_fluid=250, n_bed=1)

ot.fluid.select_substance_on_the_fly(rho=1.2, cp=700, k=0.06)
ot.fluid.select_domain_shape(domain='cylinder_1d', D=0.2, H=0.5)
ot.fluid.select_porosity(phi=0.9)
ot.fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
ot.fluid.select_initial_conditions(T=800+273.15, mdot=0.01) #CHECK
ot.fluid.select_bc(bc_type='dirichlet', parameter='T', position=(slice(None, None, None), 0), value=100+273.15)
ot.fluid.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))

ot.bed.select_substance_on_the_fly(rho=5150, cp=700, k=1)
ot.bed.select_domain_shape(domain='lumped', V=4/3*np.pi*0.005**3, A=4*np.pi*0.005**2)
ot.bed.select_initial_conditions(T=800+273.15)
#ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), 0))
#ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))

ot.select_coupling(h_coeff='constant', h_value=100)
ot.output_animation(save_int=4000)
ot.run_simulation()