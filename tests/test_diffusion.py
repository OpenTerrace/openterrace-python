import openterrace
import numpy as np
import matplotlib.pyplot as plt

def test_diffusion():
    n = 20
    t_end = 200

    Lc = 0.025
    T_init = 0
    T_inf = 100
    h = 200
    cp = 4179
    rho = 993
    k = 0.627

    ot = openterrace.GlobalParameters(t_end=t_end, dt=1e-2, n_bed=n)
    ot.bed.define_substance_on_the_fly(cp=cp, rho=rho, k=k)
    ot.bed.select_domain(domain='1d_sphere', R=Lc)
    ot.bed.select_schemes(diff='central_difference_1d')
    ot.bed.initialise(T=T_init)
    ot.bed.define_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), 0))
    ot.bed.define_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))
    ot.bed.define_source_term(source_type='thermal_resistance', R=1/(h*4*np.pi*Lc**2), T_inf=T_inf, position=(slice(None, None, None), -1))
    ot.run_simulation()

    Bi = h*Lc/k
    Fo = k/(rho*cp)*t_end/Lc**2

    r_r0_ana, theta_ana = openterrace.analytical_sphere(Bi, Fo, n)
    r_r0_num, theta_num = ot.bed.domain.node_pos/(ot.bed.domain.node_pos[-1]-ot.bed.domain.node_pos[0]), (ot.bed.T[0,:]-T_inf)/(T_init-T_inf)

    np.testing.assert_array_almost_equal(theta_ana, theta_num, decimal=2)

    plt.plot(r_r0_num, theta_num,'s', label='OpenTerrace', color = '#4cae4f')
    plt.plot(r_r0_ana, theta_ana,'k', label='Analytical')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.grid()
    plt.legend([r"OpenTerrace "+"("+r"$Bi=$"+f"{Bi:.2e}"+", "+r"$Fo=$"+f"{Fo:.2e}"+")", "Analytical"], loc ="lower left")
    plt.xlabel(r'Radial position, $r^* = r/r_0$')
    plt.ylabel(r'Temperature, $\theta = (T(r,t)-T_\infty)/(T_{init}-T_\infty)$')
    plt.savefig('docs/_figures/test_sphere_0.svg', bbox_inches='tight')