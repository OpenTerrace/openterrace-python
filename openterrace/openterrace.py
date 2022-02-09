# Standard Python modules
import sys
import numpy as np
import matplotlib.pyplot as plt

# Open Terrace modules
import profilers
import parameters
import models
import solvers

if __name__ == '__main__':
    profiling = profilers.Profiling()

    params = parameters.Parameters()
    params.read_input_data(inputfile='simulations/example.yaml', storagefolder='simulations')
    params.initialise_case(overwrite=True)

    fluid = parameters.Fluid(params)
    fluid.initialise_temp(method='const', T=303.15)
    fluid.update_props()
    fluid.update_mdot(params.timeseries_mdot, params.t)
    fluid.update_Tin(params.timeseries_Tin, params.t)

    particle = parameters.Particle(params)
    particle.initialise_temp(method='const', T=293.15)
    particle.update_props()

    model_particle = models.Particle(params, particle)
    model_particle.A_assembly()
    model_particle.b_assembly(fluid.T)
    particle.T = solvers.tridiagonal(model_particle.A, model_particle.b)

    sys.exit()

    model_tank = models.Tank(params, fluid)
    model_tank.select_schemes(conv='upwind', diff='central_difference')

    for params.t in params.t_array:
        model_particle.advance_time()
        model_tank.advance_time()
        model_tank.apply_bcs()
        
    # Update old temperatures
    particle.Told = particle.T
    fluid.Told = fluid.T

    sys.exit()

    # profiling.start()
    # profiling.end()