#Standard Python modules
import sys
import numpy as np
import matplotlib.pyplot as plt

#Open Terrace modules
import profilers
import parameters
import solvers

if __name__ == '__main__':
    profiling = profilers.Profiling()

    params = parameters.Parameters()
    params.read_input_data(inputfile='simulations/benchmark1.yaml')
    params.initialise_case(overwrite=True)

    fluid = parameters.Fluid(params)
    fluid.update_props(method='constprops', T=293.15)

    particle = parameters.Particle(params)
    particle.update_props(method='constprops', T=293.15)

    solver_tank = solvers.Tank(params, fluid)
    solver_tank.select_schemes(conv='upwind', diff='central_difference')

    solver_particle = solvers.Particle(params, particle)

    fluid.u = 0.5
    fluid.T = np.zeros_like(fluid.T)

    profiling.start()

    for params.t in np.linspace(0,params.t_end,int(params.t_end/(params.dt)+1)):
        solver_tank.update_lower_bc()
        solver_tank.eq()

    profiling.end()

    plt.plot(solver_tank.yc,fluid.T[1:-1],'-sk')
    plt.grid()
    plt.show()