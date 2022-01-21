#Standard modules
import sys
import numpy as np
import matplotlib.pyplot as plt

#Open Terrace modules
import profilers
import parameters
import particle_models
import tank_models


if __name__ == '__main__':
    params = parameters.Parameters()
    params.read_input_data(inputfile='openterrace/simulation_data/benchmark1.yaml')
    
    fluid = parameters.Fluid(params)
    particle = parameters.Particle(params)

    

    #tank_model = tank_models.ConvDiff1DExp(params)
    #tank_model.solve_eq()

    #params.update_massflow_rate(t)
    #params.update_inlet_temperature(t)

    sys.exit()

    profiling = profilers.Profiling()
    
    diff_1d = particle_models.Diff1D(const, prop)
    A0 = diff_1d.matrix_assembly_tri(const, particle)
    A = diff_1d.update_A(const, particle, A0)

    Tm0 = particle.T_old

    profiling.start()

    for t in range(0, int(const.t_end/const.dt)):
        b = diff_1d.update_b(const, particle, fluid, Tm0)
        Tm0 = diff_1d.solve_tridiagonal(A, b)

    profiling.end()

    # diff_1d.analytical(const, particle)
    # plt.plot(diff_1d.r/(const.d_p/2),Tm0,'-s',diff_1d.r/(const.d_p/2),diff_1d.theta*(const.Tinit-const.Tfluid)+const.Tfluid,'-')
    # plt.grid()
    # plt.show()