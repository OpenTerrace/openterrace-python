import numpy as np

class Constants():
    def __init__(self):
        self.dt = 2
        self.t_end = 3600
        self.h_tank = 2

        self.nx_tank = 7
        self.nx_particles = 10

        self.d_p = 2e-2
        self.phi_p = 0.3

        self.Tinit = 40
        self.Tin = 60

        self.u = np.array([0.1])

class Var():
    class Fluid():
        def __init__(self, params):
            self.T = np.full(params.nx_tank, params.Tinit)
            #self.h = np.zeros(params.nx_tank)

    class Particle():
        def __init__(self, params):
            self.T = np.full((params.nx_particles, params.nx_tank), params.Tinit)