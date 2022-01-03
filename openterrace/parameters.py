import numpy as np

class Constants():
    def __init__(self):
        self.dt = 1
        self.t_end = 900
        self.h_tank = 2

        self.nx_tank = 100
        self.nx_particles = 200

        self.d_p = 2e-2
        self.phi_p = 0.3

        self.Tinit = 40
        self.Tfluid = 12

        self.u = np.array([0.1])
        self.bc = 'forced_convection'

class Var():
    class Fluid():
        def __init__(self, const, prop):
            self.T = np.full(const.nx_tank, const.Tfluid)
            self.T_old = np.copy(self.T)
            self.rho = prop.fluid.rho(self.T)

    class Particle():
        def __init__(self, const, prop):
            self.T = np.full((const.nx_particles, const.nx_tank), const.Tinit)
            self.T_old = np.copy(self.T)
            self.rho = prop.solid.rho(self.T)
            self.k = prop.solid.k(self.T)
            self.cp = prop.solid.cp(self.T)
            self.bc = const.bc
            self.h = np.full(const.nx_tank, 200)
