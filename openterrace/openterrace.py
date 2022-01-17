import numpy as np
import matplotlib.pyplot as plt

import properties
import parameters
import particle_models
import tank_models
import profilers

if __name__ == '__main__':
    const = parameters.Constants()

    prop =  properties.Properties()
    prop.select_fluid('water')
    prop.select_solid('stone')
    prop.select_shape('sphere')

    fluid = parameters.Var.Fluid(const, prop)
    particle = parameters.Var.Particle(const, prop)

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