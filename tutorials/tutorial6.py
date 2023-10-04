""" This example sets up a water tank with PCM material as the bed material. """

import openterrace

ot = openterrace.Simulate(t_end=5400, dt=0.05, sim_name='tutorial6')

ot.fluid = ot.Phase(n=100, type='fluid')
ot.fluid.select_substance(substance='water')
ot.fluid.select_domain_shape(domain='cylinder_1d', D=0.1, H=1)
ot.fluid.select_porosity(phi=0.4)
ot.fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
ot.fluid.select_initial_conditions(T=273.15+20, mdot=0.01)
ot.fluid.select_bc(bc_type='fixedValue', parameter='T', position=(slice(None, None, None), 0), value=273.15+80)
ot.fluid.select_bc(bc_type='zeroGradient', parameter='T', position=(slice(None, None, None), -1))
ot.fluid.select_output(times=[30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570, 600, 900, 1800, 3600, 5400], parameters=['T'])

ot.bed = ot.Phase(n=20, n_other=100, type='bed')
ot.bed.select_substance('ATS58')
ot.bed.select_domain_shape(domain='hollow_sphere_1d', Rinner=0.005, Router=0.025)
ot.bed.select_schemes(diff='central_difference_1d')
ot.bed.select_initial_conditions(T=273.15+20)
ot.bed.select_bc(bc_type='zeroGradient', parameter='T', position=(slice(None, None, None), 0))
ot.bed.select_bc(bc_type='zeroGradient', parameter='T', position=(slice(None, None, None), -1))
ot.bed.select_output(times=list(range(0,5400,60)), parameters=['T'])

ot.select_coupling(fluid_phase=0, bed_phase=1, h_exp='constant', h_value=200)

ot.run_simulation()
ot.generate_plots()
ot.generate_animations()