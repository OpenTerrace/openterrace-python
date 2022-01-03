import numpy as np
import matplotlib.pyplot as plt
import cProfile, pstats, io
from pstats import SortKey

import properties
import parameters
import solvers
import plots

if __name__ == '__main__':
    const = parameters.Constants()

    prop =  properties.Properties()
    prop.select_fluid('water')
    prop.select_solid('stone')
    prop.select_shape('sphere')

    fluid = parameters.Var.Fluid(const, prop)
    particle = parameters.Var.Particle(const, prop)
    
    diff_1d = solvers.Diff1D(const, prop)
    A0 = diff_1d.matrix_assembly_tri(const, particle)
    A = diff_1d.update_A(const, particle, A0)

    Tm0 = particle.T_old

    pr = cProfile.Profile()
    pr.enable()

    for t in range(0,int(const.t_end/const.dt)):
        b = diff_1d.update_b(const, particle, fluid, Tm0)
        Tm0 = diff_1d.solve_tridiagonal(A, b)

    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

    # diff_1d.analytical(const, particle)
    # plt.plot(diff_1d.r/(const.d_p/2),Tm0,'-s',diff_1d.r/(const.d_p/2),diff_1d.theta*(const.Tinit-const.Tfluid)+const.Tfluid,'-')
    # plt.grid()
    # plt.show()