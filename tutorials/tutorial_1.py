import openterrace

ot = openterrace.GlobalParameters(t_end=50, dt=0.01, n_bed=50)

ot.bed.select_substance('magnetite')
ot.bed.select_domain_shape(domain='sphere_1d', R=0.01)
ot.bed.select_schemes(diff='central_difference_1d')
ot.bed.select_initial_conditions(T=273.15+40)
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), 0))
ot.bed.select_bc(bc_type='dirichlet', parameter='T', position=(slice(None, None, None), -1), value=273.15+80)

ot.animate(save_int=20, animate_data_flag=True)
ot.run_simulation()