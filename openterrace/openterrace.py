# Standard Python modules
import sys
import numpy as np
import matplotlib.pyplot as plt

# Open Terrace modules
import profilers
import parameters
import solvers

if __name__ == '__main__':
    profiling = profilers.Profiling()

    params = parameters.Parameters()
    params.read_input_data(inputfile='simulations/debugging.yaml', storagefolder='simulations')
    params.initialise_case(overwrite=True)

    fluid = parameters.Fluid(params)
    fluid.initialise_temp(method='const', T=303.15)
    fluid.update_props()

    particle = parameters.Particle(params)
    particle.initialise_temp(method='const', T=293.15)
    particle.update_props()

    solver_tank = solvers.Tank(params, fluid)
    solver_tank.select_schemes(conv='upwind', diff='central_difference')

    solver_particle = solvers.Particle(params, particle)
    solver_particle.A_assembly()

    solver_particle.b_assembly(fluid.T)
    particle.T = solver_particle.solve_eq(A=solver_particle.A, b=solver_particle.b)

    # profiling.start()

    # for params.t in np.linspace(0,params.t_end,int(params.t_end/(params.dt)+1)):
    #     pass
    #     # solver_tank.update_lower_bc()
    #     # solver_tank.solve_eq()

    # profiling.end()

    # diff_1d.analytical(const, particle)
    # plt.plot(diff_1d.r/(const.d_p/2),Tm0,'-s',diff_1d.r/(const.d_p/2),diff_1d.theta*(const.Tinit-const.Tfluid)+const.Tfluid,'-')
    # plt.grid()
    # plt.show()