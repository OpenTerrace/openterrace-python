import openterrace
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pytest
import sys

def test_heat_diffusion_wall():
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

    ot3 = openterrace.Simulate(t_end=t_end, dt=1e-2)
    bed = ot3.create_phase(n=n, type='bed')
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
    ot3.run_simulation()

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
    plt.savefig('ot_test_heat_diffusion_wall.svg', bbox_inches='tight')
    plt.close()

    np.testing.assert_array_almost_equal(theta_ana, theta_num, decimal=2)