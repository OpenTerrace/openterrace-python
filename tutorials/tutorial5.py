""" 
This example shows how to simulate a cylindrical
thermal storage tank with air and spherical magnetite
stones as the bed material. The tank has a diameter of
30 cm and a height of 1 m. The initial temperature of
the air is 25℃. The air is heated up to 500℃ at the
bottom. Heat transfer from the fluid phase to the bed
phase is modelled with a constant heat transfer coefficient
of 100 W/m²K. The simulation time is 10 hours, and the
output is saved every hour.
"""

import openterrace
import matplotlib.pyplot as plt

def main():
    t_end = 3600*10

    ot = openterrace.Simulate(t_end=t_end, dt=0.02)

    fluid = ot.create_phase(n=50, type='fluid')
    fluid.select_substance(substance='air')
    fluid.select_domain_shape(domain='cylinder_1d', D=0.3, H=1)
    fluid.select_porosity(phi=0.4)
    fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
    fluid.select_initial_conditions(T=273.15+25)
    fluid.select_massflow(mdot=0.01)
    fluid.select_bc(bc_type='fixed_value',
                    parameter='T',
                    position=(slice(None, None, None), 0),
                    value=273.15+500
                    )
    fluid.select_bc(bc_type='zero_gradient',
                    parameter='T',
                    position=(slice(None, None, None), -1)
                    )
    fluid.select_output(times=range(0, t_end+3600, 3600))

    bed = ot.create_phase(n=20, n_other=50, type='bed')
    bed.select_substance(substance='magnetite')
    bed.select_domain_shape(domain='sphere_1d', R=0.05)
    bed.select_schemes(diff='central_difference_1d')
    bed.select_initial_conditions(T=273.15+25)
    bed.select_bc(bc_type='zero_gradient',
                parameter='T',
                position=(slice(None, None, None), 0))
    bed.select_bc(bc_type='zero_gradient',
                parameter='T',
                position=(slice(None, None, None), -1))
    bed.select_output(times=range(0, t_end+3600, 3600))

    ot.select_coupling(fluid_phase=0, bed_phase=1, h_exp='constant', h_value=100)
    ot.run_simulation()

    plt.plot(fluid.node_pos,fluid.data.T[:,0,:].T-273.15, label=fluid.data.time/3600)
    plt.legend(title='Simulation time (h)')
    plt.show()
    plt.xlabel(u'Cylinder position (m)')
    plt.ylabel(u'Temperature (℃)')
    plt.grid()
    plt.grid(which='major', color='#DDDDDD', linewidth=1)
    plt.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.8)
    plt.minorticks_on()
    plt.savefig('ot_plot_tutorial5.svg')

if __name__ == "__main__":
    main()