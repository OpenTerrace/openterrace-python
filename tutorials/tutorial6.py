""" This example sets up a water tank with PCM material as the bed material. """

import openterrace

ot = openterrace.Simulate(t_end=3600*2, dt=0.05, sim_name='tutorial6')

fluid = ot.createPhase(n=100, type='fluid')
fluid.select_substance(substance='water')
fluid.select_domain_shape(domain='cylinder_1d', D=0.1, H=1)
fluid.select_porosity(phi=0.4)
fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
fluid.select_initial_conditions(T=273.15+20, mdot=0.01)
fluid.select_bc(bc_type='fixedValue', parameter='T', position=(slice(None, None, None), 0), value=273.15+80)
fluid.select_bc(bc_type='zeroGradient', parameter='T', position=(slice(None, None, None), -1))
fluid.select_output(times=[30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570, 600, 900, 1800, 3600, 5400], parameters=['T'])

bed = ot.createPhase(n=20, n_other=100, type='bed')
bed.select_substance('ATS58')
bed.select_domain_shape(domain='hollow_sphere_1d', Rinner=0.005, Router=0.025)
bed.select_schemes(diff='central_difference_1d')
bed.select_initial_conditions(T=273.15+20)
bed.select_bc(bc_type='zeroGradient', parameter='T', position=(slice(None, None, None), 0))
bed.select_bc(bc_type='zeroGradient', parameter='T', position=(slice(None, None, None), -1))
bed.select_output(times=list(range(0,7200,300)), parameters=['T'])

ot.select_coupling(fluid_phase=0, bed_phase=1, h_exp='constant', h_value=200)
ot.run_simulation()
ot.generate_plots()
ot.generate_animations()