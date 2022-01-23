import numpy as np

class ConvDiff1DExp:
    """This class is used for modelling the tank as a 1D convection-diffusion problem with explicit 1 order temporal discretisation.
        """
    def __init__(self, params):
        self.dy = params.h_tank/(params.ny_tank)
        self.y = np.concatenate(([0], np.arange(self.dy/2,params.h_tank,self.dy), [params.h_tank/2]))

    def solve_eq(self):
        pass