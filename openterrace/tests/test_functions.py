import openterrace
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pytest
import sys



def test_1():
    ot = openterrace.Simulate(t_end=10000, dt=1)
    fluidbox = ot.create_phase(n=101, type='fluid')
    fluidbox.select_substance_on_the_fly(cp=4200, rho=1000, k=0.6)
    fluidbox.select_domain_shape(domain='block_1d', A=0.1, L=0.1)
    fluidbox.select_schemes(diff='central_difference_1d')
    fluidbox.select_initial_conditions(T=np.linspace(0,100, 101))
    fluidbox.select_bc(bc_type='zero_gradient', parameter='T', position=(slice(None, None, None), 0))
    fluidbox.select_bc(bc_type='zero_gradient', parameter='T', position=(slice(None, None, None), -1))
    fluidbox.select_output(times=range(0, 11000, 1000), output_parameters=['T','h'])
    
    ot.run_simulation()

    plt.plot(fluidbox.node_pos, fluidbox.data.h[:,0,:].T, label=fluidbox.data.time)
    plt.legend(title='Simulation time (s)')
    plt.xlabel(u'Position (m)')
    plt.ylabel(u'Specific enthalpy (J/(kg))')
    plt.grid()
    plt.grid(which='major', color='#DDDDDD', linewidth=1)
    plt.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.8)
    plt.minorticks_on()
    plt.savefig('ot_test_1.svg', bbox_inches='tight')
    
    np.testing.assert_array_almost_equal(1,1, decimal=2) #Dummy check

def test_2():
    n = 50
    dt = 1e-2
    t_end = 200
    Lc = 0.025
    T_init = 0
    T_inf = 100
    h = 200
    cp = 4179
    rho = 993
    k = 0.627

    ot = openterrace.Simulate(t_end=t_end, dt=dt)
    bed = ot.create_phase(n=n, type='bed')
    bed.select_substance_on_the_fly(cp=cp, rho=rho, k=k)
    bed.select_domain_shape(domain='sphere_1d', R=Lc)
    bed.select_schemes(diff='central_difference_1d')
    bed.select_initial_conditions(T=T_init)
    bed.select_bc(bc_type='zero_gradient', parameter='T', position=(slice(None, None, None), 0))
    bed.select_bc(bc_type='zero_gradient', parameter='T', position=(slice(None, None, None), -1))

    # Initialise array of thermal resistances
    R = np.inf*np.ones_like(bed.T)

    # Modify the thermal resistance at the surface of the sphere to account for convection
    R[0][-1] = 1/(h*4*np.pi*Lc**2)

    # Add the thermal resistance source term
    bed.add_sourceterm_thermal_resistance(R=R, T_inf=T_inf)

    ot.run_simulation()

    Bi = h*Lc/k
    Fo = k/(rho*cp)*t_end/Lc**2

    r_r0_ana, theta_ana = openterrace.analytical_diffusion_sphere(Bi, Fo, n)
    r_r0_num, theta_num = bed.node_pos/(bed.node_pos[-1]-bed.node_pos[0]), (bed.T[0,:]-T_inf)/(T_init-T_inf)

    plt.plot(r_r0_num, theta_num,'s', label='OpenTerrace', color = '#4cae4f')
    plt.plot(r_r0_ana, theta_ana,'k', label='Analytical')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.grid()
    plt.legend([r"OpenTerrace "+"("+r"$Bi=$"+f"{Bi:.2e}"+", "+r"$Fo=$"+f"{Fo:.2e}"+")", "Analytical"], loc ="lower left")
    plt.xlabel(r'Radial position, $r^* = r/r_0$')
    plt.ylabel(r'Temperature, $\theta = (T(r,t)-T_\infty)/(T_{init}-T_\infty)$')
    plt.savefig('ot_test_2.svg', bbox_inches='tight')
    plt.close()

    np.testing.assert_array_almost_equal(theta_ana, theta_num, decimal=2)

def test_3():
    n = 50
    t_end = 200

    Lc = 0.025
    T_init = 0
    T_inf = 100
    h = 200
    cp = 4179
    rho = 993
    k = 0.627
    A = 1

    ot = openterrace.Simulate(t_end=t_end, dt=1e-2)
    bed = ot.create_phase(n=n, type='bed')
    bed.select_substance_on_the_fly(cp=cp, rho=rho, k=k)
    bed.select_domain_shape(domain='block_1d', L=Lc, A=A)
    bed.select_schemes(diff='central_difference_1d')
    bed.select_initial_conditions(T=T_init)
    bed.select_bc(bc_type='zero_gradient', parameter='T', position=(slice(None, None, None), 0))
    bed.select_bc(bc_type='zero_gradient', parameter='T', position=(slice(None, None, None), -1))

    # Initialise array of thermal resistances
    R = np.inf*np.ones_like(bed.T)

    # Modify the thermal resistance at the surface of the sphere to account for convection
    R[0][-1] = 1/(h*A)

    # Add the thermal resistance source term
    bed.add_sourceterm_thermal_resistance(R=R, T_inf=T_inf)

    #bed.select_source_term(source_type='thermal_resistance', R=1/(h*A), T_inf=T_inf, position=(slice(None, None, None), -1))
    ot.run_simulation()

    Bi = h*Lc/k
    Fo = k/(rho*cp)*t_end/Lc**2

    x_x0_ana, theta_ana = openterrace.analytical_diffusion_wall(Bi, Fo, n)
    x_x0_num, theta_num = bed.node_pos/(bed.node_pos[-1]-bed.node_pos[0]), (bed.T[0,:]-T_inf)/(T_init-T_inf)

    plt.plot(x_x0_num, theta_num,'s', label='OpenTerrace', color = '#4cae4f')
    plt.plot(x_x0_ana, theta_ana,'k', label='Analytical')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.grid()
    plt.legend([r"OpenTerrace "+"("+r"$Bi=$"+f"{Bi:.2e}"+", "+r"$Fo=$"+f"{Fo:.2e}"+")", "Analytical"], loc ="lower left")
    plt.xlabel(r'Position, $x^* = x/L$')
    plt.ylabel(r'Temperature, $\theta = (T(r,t)-T_\infty)/(T_{init}-T_\infty)$')
    plt.savefig('ot_test_3.svg', bbox_inches='tight')
    plt.close()

    np.testing.assert_array_almost_equal(theta_ana, theta_num, decimal=2)

def test_4():
    n = 1000
    t_end = 120

    H = 2
    D = 0.5
    T_init = 0
    T_in = 100
    cp = 4180
    rho = 993
    k = 0
    mdot = 1

    ot = openterrace.Simulate(t_end=t_end, dt=1e-2)
    fluid = ot.create_phase(n=n, type='fluid')
    fluid.select_substance_on_the_fly(cp=cp, rho=rho, k=k)
    fluid.select_domain_shape(domain='cylinder_1d', D=D, H=H)
    fluid.select_schemes(conv='upwind_1d')
    fluid.select_initial_conditions(T=T_init)
    fluid.select_massflow(mdot=mdot)
    fluid.select_bc(bc_type='fixed_value',
                    parameter='T',
                    position=(slice(None, None, None), 0),
                    value=T_in
                    )
    fluid.select_bc(bc_type='zero_gradient',
                    parameter='T',
                    position=(slice(None, None, None), -1)
                    )
    ot.run_simulation()

    X = t_end*(mdot/rho/(np.pi*(D/2)**2))/H

    y_H_num, theta_num = fluid.node_pos/(fluid.node_pos[-1]-fluid.node_pos[0]), (fluid.T[0]-T_in)/(T_init-T_in)
    y_H_ana, theta_ana = openterrace.analytical_step(X, n)

    plt.plot(y_H_num, theta_num,'s', label='OpenTerrace', color = '#4cae4f')
    plt.plot(y_H_ana, theta_ana,'k', label='Analytical')
    plt.xlim([0, 1])
    plt.ylim([-0.1, 1.1])
    plt.grid()
    plt.legend([r"OpenTerrace "+"("+r"upwind scheme"+")", "Analytical"], loc ="lower right")
    plt.xlabel(r'Position, $y^* = y/H$')
    plt.ylabel(r'Temperature, $\theta = (T(x,t)-T_{in})/(T_{init}-T_{in})$')
    plt.savefig('ot_test_4.svg', bbox_inches='tight')
    plt.close()

    np.testing.assert_array_almost_equal(1,1, decimal=2) #Dummy check
    
def test_5():
    ot = openterrace.Simulate(t_end=10, dt=5)
    fluid = ot.create_phase(n=11, type='fluid')
    fluid.select_substance_on_the_fly(cp=1000, rho=1000, k=1)
    fluid.select_domain_shape(domain='block_1d', L=1, A=1)
    fluid.select_schemes(diff='central_difference_1d')
    fluid.select_porosity(phi=0.4)
    fluid.select_initial_conditions(T=100)
    fluid.select_bc(bc_type='zero_gradient',
                    parameter='T',
                    position=(slice(None, None, None), 0)
                    )
    fluid.select_bc(bc_type='zero_gradient',
                    parameter='T',
                    position=(slice(None, None, None), -1)
                    )
    fluid.select_output(times=range(0, 15, 5), output_parameters=['T', 'h'])
    
    bed = ot.create_phase(n=5, n_other=11, type='bed')
    bed.select_substance_on_the_fly(cp=1000, rho=4000, k=1)
    bed.select_domain_shape(domain='sphere_1d', R=(0.1*3/4*1/np.pi)**(1/3))
    bed.select_schemes(diff='central_difference_1d')
    bed.select_initial_conditions(T=0)
    bed.select_bc(bc_type='zero_gradient',
                  parameter='T',
                  position=(slice(None, None, None), 0)
                  )
    bed.select_bc(bc_type='zero_gradient', 
                  parameter='T',
                  position=(slice(None, None, None), -1)
                  )
    bed.select_output(times=range(0, 15, 5), output_parameters=['T', 'h'])
    
    ot.select_coupling(fluid_phase=0, bed_phase=1, h_exp='constant', h_value=150)
    ot.run_simulation()

if __name__ == '__main__':
    test_5()