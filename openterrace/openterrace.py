import numpy as np
import matplotlib.pyplot as plt
import pathlib
import timeit
import sys

import properties
import parameters
import solvers
import plots

if __name__ == '__main__':
    const = parameters.Constants()
    fluid = parameters.Var.Fluid(const)
    particle = parameters.Var.Particle(const)

    prop =  properties.Properties()
    prop.select_fluid('water')
    prop.select_solid('stone')
    prop.select_shape('sphere')

    diff_1d = solvers.Diff1D(const)
    #diff_1d.matrix_assembly_tri(prop, particle)

    #print(const.d_p)
    sys.exit()
        #convection_diffusion_1d = solvers.ConvectionDiffusion1D(u, alpha_f, y[0], y[-1], ny, dt)
        #convection_diffusion_1d.matrix_assembly(scheme='upwind')
        # convection_diffusion_1d.A[0][0] = 1
        # print(convection_diffusion_1d.A)
    
    diff_1d.update_bc(bc_particle='forced_convection', h=200)

    start = timeit.default_timer()
    for t in range(0,int(params.t_end/params.dt)):
        T_m = diffusion_1d.matrix_solve_tri(T_m0=T_m0, T_f0=12)
        T_m0 = T_m
    end = timeit.default_timer()
    print('Simulation time was:', end-start, 's')
        
        # diffusion_1d.analytical()

        # plt.plot(diffusion_1d.r/(params.dp/2),T_m0,'-s',diffusion_1d.r/(params.dp/2),diffusion_1d.theta*(Tinit-12)+12,'-')
        # plt.grid()
        # plt.show()