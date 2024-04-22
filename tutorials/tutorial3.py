"""
This example shows how to simulate heat diffusion
in a sphere made out of swedish diabase stone.
The sphere has a radius of 2.5 cm, and the initia 
temperature is 40℃. The sphere is exposed to a 
convection heat transfer with a heat transfer 
coefficient of 200 W/m²K. The simulation time 
is 15 minutes, and the output is saved every 60 seconds.
"""

import openterrace
import matplotlib.pyplot as plt
import numpy as np

def main():
    D = 0.05
    T_init = 40+273.15
    T_inf = 80+273.15
    h = 200

    ot = openterrace.Simulate(t_end=15*60, dt=0.01)

    bed = ot.create_phase(n=50, type='bed')
    bed.select_substance('swedish_diabase')
    bed.select_domain_shape(domain='sphere_1d', R=D/2)
    bed.select_schemes(diff='central_difference_1d')
    bed.select_initial_conditions(T=T_init)
    bed.select_bc(bc_type='zero_gradient', 
                parameter='T', 
                position=(slice(None, None, None), 0))
    bed.select_bc(bc_type='zero_gradient', 
                parameter='T',
                position=(slice(None, None, None), -1))
                
    # Initialise array of thermal resistances
    R = np.inf*np.ones_like(bed.T)

    # Set thermal resistance for the surface
    R[0][-1] = 1/(h*4*np.pi*(D/2)**2)

    bed.add_sourceterm_thermal_resistance(R=R, T_inf=T_inf)
    bed.select_output(times=range(0, 15*60+60, 60))

    ot.run_simulation()

    plt.plot(bed.node_pos,bed.data.T[:,0,:].T-273.15, label=bed.data.time)
    plt.legend(title='Simulation time (s)')
    plt.show()
    plt.xlabel(u'Sphere radial position (m)')
    plt.ylabel(u'Temperature (℃)')
    plt.grid()
    plt.grid(which='major', color='#DDDDDD', linewidth=1)
    plt.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.8)
    plt.minorticks_on()
    plt.savefig('ot_plot_tutorial3.svg')

if __name__ == "__main__":
    main()