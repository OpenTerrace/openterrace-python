""" 
This example shows how a cylindrical pit storage looses
energy to the surroundings over a period of 30 days.
"""

import openterrace
import matplotlib.pyplot as plt
import numpy as np

D = 2
R = D/2
H = 10
T_inf = 273.15+10

def main():
    ot = openterrace.Simulate(t_end=3600*24*30, dt=5)

    fluid = ot.create_phase(n=101, type='fluid')
    fluid.select_substance_on_the_fly(rho=1000, cp=4200, k=0.6)
    fluid.select_domain_shape(domain='cylinder_1d', D=D, H=H)
    fluid.select_schemes(diff='central_difference_1d')
    fluid.select_initial_conditions(T=273.15+80)
    fluid.select_bc(bc_type='zero_gradient', 
                    parameter='T', 
                    position=(slice(None, None, None), 0)
                    )
    fluid.select_bc(bc_type='zero_gradient', 
                    parameter='T', 
                    position=(slice(None, None, None), -1)
                    )
    fluid.select_output(times=range(0, 3600*24*60+3600*24, 3600*24*2))

    # Calculate surface area of each node
    As = fluid.domain.dx*np.pi*D

    # Correct bottom node because its only half the height of the other nodes
    As[0] = As[0]/2 + np.pi*(D/2)**2

    # Correct top node because its only half the height of the other nodes
    As[-1] = As[-1]/2 + np.pi*(D/2)**2

    # Overall heat transfer coefficient
    U = 10

    # Thermal resistance
    R = 1/(U*As)

    fluid.add_sourceterm_thermal_resistance(R=R, T_inf=T_inf)

    ot.run_simulation()

    plt.plot(fluid.node_pos,fluid.data.T[:,0,:].T-273.15, label=fluid.data.time/(3600*24))
    plt.legend(title='Simulation time (day)')
    plt.show()
    plt.xlabel(u'Height (m)')
    plt.ylabel(u'Temperature (℃)')
    plt.grid()
    plt.grid(which='major', color='#DDDDDD', linewidth=1)
    plt.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.8)
    plt.minorticks_on()
    plt.savefig('ot_plot_tutorial6.svg')

if __name__ == "__main__":
    main()