import openterrace

ot = openterrace.GlobalParameters(t_end=60*15, dt=1, n_fluid=50)

ot.fluid.select_substance_on_the_fly(rho=1000, cp=4200, k=0.6)
ot.fluid.select_domain_shape(domain='cylinder_1d', D=0.3, H=1)
ot.fluid.select_porosity(phi=0.4)
ot.fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
ot.fluid.select_initial_conditions(T=273.15+100, mdot=0.05)
ot.fluid.select_bc(bc_type='dirichlet', parameter='T', position=(slice(None, None, None), 0), value=273.15+600)
ot.fluid.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))

ot.animate(save_int=5, animate_data_flag=True)
ot.run_simulation()