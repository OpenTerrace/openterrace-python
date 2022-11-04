import openterrace
import matplotlib.pyplot as plt
import numpy as np

ot = openterrace.GlobalParameters(t_end=3600*1, dt=0.1, n_bed=50)

ot.bed.select_substance('ATS58')
ot.bed.select_domain(domain='1d_sphere', R=0.05)
ot.bed.select_schemes(diff='central_difference_1d')
ot.bed.initialise(T=273.15+40)
ot.bed.define_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), 0))
ot.bed.define_bc(bc_type='dirichlet', parameter='T', position=(slice(None, None, None), -1), value=273.15+80)

ot.animate(animate_data_flag=True, save_int=100)
ot.run_simulation()