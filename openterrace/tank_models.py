import numpy as np

class ConvDiff1DExp:
    """This class is used for modelling the tank as a 1D convection-diffusion problem with explicit 1 order temporal discretisation.
        """
    def __init__(self, params):
        self.const = const
        self.fluid = fluid
        self.dx = const.h_tank/(const.nx_tank)
        self.x = np.concatenate(([0], np.arange(self.dx/2,const.h_tank,self.dx), [const.h_tank/2]))

    def solve_eq(self):
        self.fluid.new 