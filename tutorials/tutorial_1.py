import openterrace
import matplotlib.pyplot as plt
import numpy as np

ot = openterrace.GlobalParameters(t_end=3600*10, dt=0.1, n_fluid=50, n_bed=10)

ot.fluid.select_substance('air')
ot.fluid.select_domain(domain='1d_cylinder', D=1, H=5)
ot.fluid.add_porosity(phi=0.4)
ot.fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
ot.fluid.initialise(T=273.15+20, mdot=0.1)
ot.fluid.define_bc(bc_type='dirichlet', parameter='T', position=(slice(None, None, None), 0), value=273.15+50)
ot.fluid.define_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))

ot.bed.select_substance('magnetite')
ot.bed.select_domain(domain='1d_sphere', R=0.01)
ot.bed.select_schemes(diff='central_difference_1d')
ot.bed.initialise(T=273.15+20)
ot.bed.define_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), 0))
ot.bed.define_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))

ot.define_coupling(h_coeff='constant', h_value=5)
ot.run_simulation()

plt.plot(ot.fluid.domain.node_pos,np.mean(ot.bed.T,1))
plt.plot(ot.fluid.domain.node_pos,ot.fluid.T[0])
plt.grid()
plt.show()