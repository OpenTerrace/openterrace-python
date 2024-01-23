""" 
This example shows how to simulate a cylindrical thermal storage tank with air and spherical magnetite
stones as the bed material. Same as other tutorial but with lumped stones.
"""

import openterrace

t_end = 3600*1

ot = openterrace.Simulate(t_end=t_end, dt=0.05, sim_name='tutorial6')

fluid = ot.createPhase(n=50, type='fluid')
fluid.select_substance(substance='air')
fluid.select_domain_shape(domain='cylinder_1d', D=0.3, H=1)
fluid.select_porosity(phi=0.4)
fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
fluid.select_initial_conditions(T=273.15+25)
fluid.select_massflow(mdot=0.001)
fluid.select_bc(bc_type='fixedValue',
                   parameter='T',
                   position=(slice(None, None, None), 0),
                   value=273.15+500
                   )
fluid.select_bc(bc_type='zeroGradient',
                   parameter='T',
                   position=(slice(None, None, None), -1)
                   )
fluid.select_output(times=range(0, t_end+600, 600))
 
bed = ot.createPhase(n=1, n_other=50, type='bed')
bed.select_substance(substance='magnetite')
bed.select_domain_shape(domain='lumped', A=4*3.14159*0.05**2, V=4/3*3.14159*0.05**3)

bed.select_initial_conditions(T=273.15+25)
bed.select_output(times=range(0, t_end+600, 600))

ot.select_coupling(fluid_phase=0, bed_phase=1, h_exp='constant', h_value=100)
ot.run_simulation()

ot.generate_plot(x=fluid.node_pos, y=fluid.data.T, times=fluid.data.time, xlabel='Position', ylabel='Temperature', name='fig1')
ot.generate_plot(x=bed.node_pos, y=bed.data.T, times=bed.data.time, xlabel='Position', ylabel='Temperature', name='fig2')