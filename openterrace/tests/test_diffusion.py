import openterrace
import numpy as np
import matplotlib.pyplot as plt
import datetime

def test_diffusion_sphere():
    n = 50
    t_end = 200

    Lc = 0.025
    T_init = 0
    T_inf = 100
    h = 200
    cp = 4179
    rho = 993
    k = 0.627

    ot = openterrace.Simulate(t_end=t_end, dt=1e-2)
    ot.bed = ot.Phase(n=n, type='bed')
    ot.bed.select_substance_on_the_fly(cp=cp, rho=rho, k=k)
    ot.bed.select_domain_shape(domain='sphere_1d', R=Lc)
    ot.bed.select_schemes(diff='central_difference_1d')
    ot.bed.select_initial_conditions(T=T_init)
    ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), 0))
    ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))
    ot.bed.select_source_term(source_type='thermal_resistance', R=1/(h*4*np.pi*Lc**2), T_inf=T_inf, position=(slice(None, None, None), -1))
    ot.run_simulation()

    Bi = h*Lc/k
    Fo = k/(rho*cp)*t_end/Lc**2

    r_r0_ana, theta_ana = openterrace.analytical_sphere(Bi, Fo, n)
    r_r0_num, theta_num = ot.bed.domain.node_pos/(ot.bed.domain.node_pos[-1]-ot.bed.domain.node_pos[0]), (ot.bed.T[0,:]-T_inf)/(T_init-T_inf)

    plt.plot(r_r0_num, theta_num,'s', label='OpenTerrace', color = '#4cae4f')
    plt.plot(r_r0_ana, theta_ana,'k', label='Analytical')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.grid()
    plt.legend([r"OpenTerrace "+"("+r"$Bi=$"+f"{Bi:.2e}"+", "+r"$Fo=$"+f"{Fo:.2e}"+")", "Analytical"], loc ="lower left")
    plt.xlabel(r'Radial position, $r^* = r/r_0$')
    plt.ylabel(r'Temperature, $\theta = (T(r,t)-T_\infty)/(T_{init}-T_\infty)$')
    plt.savefig('test_diffusion_sphere.svg', bbox_inches='tight')
    plt.close()

    np.testing.assert_array_almost_equal(theta_ana, theta_num, decimal=2)

def test_diffusion_wall():
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
    ot.bed = ot.Phase(n=n, type='bed')
    ot.bed.select_substance_on_the_fly(cp=cp, rho=rho, k=k)
    ot.bed.select_domain_shape(domain='block_1d', L=Lc, A=A)
    ot.bed.select_schemes(diff='central_difference_1d')
    ot.bed.select_initial_conditions(T=T_init)
    ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), 0))
    ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))
    ot.bed.select_source_term(source_type='thermal_resistance', R=1/(h*A), T_inf=T_inf, position=(slice(None, None, None), -1))
    ot.run_simulation()

    Bi = h*Lc/k
    Fo = k/(rho*cp)*t_end/Lc**2

    x_x0_ana, theta_ana = openterrace.analytical_wall(Bi, Fo, n)
    x_x0_num, theta_num = ot.bed.domain.node_pos/(ot.bed.domain.node_pos[-1]-ot.bed.domain.node_pos[0]), (ot.bed.T[0,:]-T_inf)/(T_init-T_inf)

    plt.plot(x_x0_num, theta_num,'s', label='OpenTerrace', color = '#4cae4f')
    plt.plot(x_x0_ana, theta_ana,'k', label='Analytical')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.grid()
    plt.legend([r"OpenTerrace "+"("+r"$Bi=$"+f"{Bi:.2e}"+", "+r"$Fo=$"+f"{Fo:.2e}"+")", "Analytical"], loc ="lower left")
    plt.xlabel(r'Position, $x^* = x/L$')
    plt.ylabel(r'Temperature, $\theta = (T(r,t)-T_\infty)/(T_{init}-T_\infty)$')
    plt.savefig('test_diffusion_wall.svg', bbox_inches='tight')
    plt.close()

    np.testing.assert_array_almost_equal(theta_ana, theta_num, decimal=2)

if __name__ == "__main__":
    test_diffusion_sphere()
    test_diffusion_wall()