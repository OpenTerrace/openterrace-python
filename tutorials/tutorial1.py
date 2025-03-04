""" 
This example shows how to simulate advection of temperature
in a cylindrical tank without any bed material. At the bottom (y=0)
the temperature is fixed at 80℃ (direchlet-type BC), and at the top (y=1)
a neumann-type BC is applied. 20 nodes are used to discretize the domain.
The fluid is water, and the mass flow rate is 0.1 kg/s. The simulation
time is 600 seconds, and the output is saved every 60 seconds.
"""

import openterrace
import matplotlib.pyplot as plt

def main():
    ot = openterrace.Setup(t_simulate=600, dt=0.01)

    fluid = openterrace.Phase(type='fluid')
    fluid.select_substance_on_the_fly(rho=1000, cp=4200, k=0.6)
    fluid.select_domain_type(domain='cylinder_1d')
    fluid.create_domain(n=(10,1), D=0.1, H=1)
    fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
    fluid.select_porosity(phi=1)
    fluid.select_initial_temperature(T=273.15+20)
    fluid.select_massflow(mdot=0.1)

    fluid.select_bc(position=0, bc_type='fixed_value', value=273.15+80)
    fluid.select_bc(position=-1, bc_type='fixed_gradient', value=0)

    fluid.select_output(times=range(0, 15*60+60, 60))

    ot.run_simulation(phases=[fluid])

    print(fluid.domain.node_pos)

    plt.plot(fluid.domain.node_pos,fluid.data.parameters['T']-273.15)#, label=fluid.data.times)
    plt.legend(title='Simulation time (s)')
    plt.show()
    plt.xlabel(u'Cylinder position (m)')
    plt.ylabel(u'Temperature (℃)')
    plt.grid()
    plt.grid(which='major', color='#DDDDDD', linewidth=1)
    plt.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.8)
    plt.minorticks_on()
    plt.savefig('ot_plot_tutorial1.svg')

if __name__ == "__main__":
    main()