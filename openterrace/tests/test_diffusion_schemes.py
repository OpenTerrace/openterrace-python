import openterrace
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pytest
import sys

def test_diffusion(scheme):
    n = 50
    dt = 1e-2
    t_end = 200
    r = 0.025
    T_init = 0
    T_inf = 100
    h = 200
    cp = 4179
    rho = 993
    k = 0.627

    ot = openterrace.Setup(t_simulate=t_end, dt=dt)

    bed = openterrace.Phase(type='bed')
    bed.select_substance_on_the_fly(cp=cp, rho=rho, k=k)
    bed.select_domain_type(domain='sphere_1d')
    bed.create_domain(n=(n, 1), radius=r)
    bed.select_schemes(diff='central_difference_1d')
    bed.initialise(T=T_init)
    bed.select_bc(position=0, bc_type='fixed_gradient', value=0)
    bed.select_bc(position=-1, bc_type='fixed_gradient', value=0)

    # Initialise array of thermal resistances
    R = np.inf*np.ones_like(bed.T)

    # Modify the thermal resistance at the surface of the sphere to account for convection
    R[-1] = 1/(h*4*np.pi*r**2)

    # Add the thermal resistance source term
    bed.add_sourceterm_thermal_resistance(R=R, T_inf=T_inf)

    ot.run_simulation(phases=[bed])

    Bi = h*r/k
    Fo = k/(rho*cp)*t_end/r**2

    r_r0_ana, theta_ana = openterrace.analytical_diffusion_sphere(Bi, Fo, n)
    r_r0_num, theta_num = bed.domain.node_pos/(bed.domain.node_pos[-1]-bed.domain.node_pos[0]), (bed.T-T_inf)/(T_init-T_inf)

    plt.plot(r_r0_num, theta_num,'s', label='OpenTerrace', color = '#4cae4f')
    plt.plot(r_r0_ana, theta_ana,'k', label='Analytical')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.grid()
    plt.legend([r"OpenTerrace "+"("+r"$Bi=$"+f"{Bi:.2e}"+", "+r"$Fo=$"+f"{Fo:.2e}"+")", "Analytical"], loc ="lower left")
    plt.xlabel(r'Radial position, $r^* = r/r_0$')
    plt.ylabel(r'Temperature, $\theta = (T(r,t)-T_\infty)/(T_{init}-T_\infty)$')
    plt.savefig('ot_test_heat_diffusion_sphere.svg', bbox_inches='tight')
    plt.close()

    np.testing.assert_array_almost_equal(theta_ana, theta_num[:,0], decimal=2)

if __name__ == "__main__":
    for scheme in openterrace.diffusion_schemes.__all__:
        for domain_type in openeterrace.domain_types.__all__:
            test_diffusion(scheme, domain_type)