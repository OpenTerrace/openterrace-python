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
    ot = openterrace.Simulate(t_end=600, dt=0.01)

    fluid = ot.create_phase(n=20, type='fluid')
    fluid.select_substance_on_the_fly(rho=1000, cp=4200, k=0.6)
    fluid.select_domain_shape(domain='cylinder_1d', D=0.3, H=1)
    fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
    fluid.select_initial_conditions(T=273.15+20)
    fluid.select_massflow(mdot=0.1)
    fluid.select_bc(bc_type='fixed_value', 
                    parameter='T', 
                    position=(slice(None, None, None), 0), 
                    value=273.15+80)
    fluid.select_bc(bc_type='zero_gradient', 
                    parameter='T', 
                    position=(slice(None, None, None), -1), 
                    value=0)
    fluid.select_output(times=range(0, 15*60+60, 60))

    ot.run_simulation()

    plt.plot(fluid.node_pos,fluid.data.T[:,0,:].T-273.15, label=fluid.data.time)
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