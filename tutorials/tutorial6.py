""" 
This example shows how to simulate a cylindrical thermal storage tank with air and spherical magnetite
stones as the bed material. Same as other tutorial but with lumped stones.
"""

import openterrace

t_end = 3600*20

ot = openterrace.Simulate(t_end=t_end, dt=0.05, sim_name='tutorial6')

fluid = ot.createPhase(n=50, type='fluid')
fluid.select_substance(substance='air')
fluid.select_domain_shape(domain='cylinder_1d', D=0.3, H=1)
fluid.select_porosity(phi=0.4)
fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
fluid.select_initial_conditions(T=273.15+25, mdot=0.001)
fluid.select_bc(bc_type='fixedValue',
                   parameter='T',
                   position=(slice(None, None, None), 0),
                   value=273.15+500
                   )
fluid.select_bc(bc_type='zeroGradient',
                   parameter='T',
                   position=(slice(None, None, None), -1)
                   )
fluid.select_output(times=range(0, t_end+1800, 1800), parameters=['T'])
 
bed = ot.createPhase(n=1, n_other=50, type='bed')
bed.select_substance(substance='magnetite')
bed.select_domain_shape(domain='lumped', A=4*3.14159*0.05**2, V=4/3*3.14159*0.05**3)
bed.select_initial_conditions(T=273.15+25)
bed.select_output(times=range(0, t_end+1800, 1800), parameters=['T'])

ot.select_coupling(fluid_phase=0, bed_phase=1, h_exp='constant', h_value=100)
ot.run_simulation()
ot.generate_plot(pos_phase=bed, data_phase=bed)
ot.generate_plot(pos_phase=fluid, data_phase=fluid)
ot.generate_animation(pos_phase=fluid, data_phase=fluid)