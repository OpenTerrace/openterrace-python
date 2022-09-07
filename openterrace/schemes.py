import numpy as np
import numba as nb

class Convection:
    """Various schemes for discretising the advection term.
    """
    @nb.njit
    def upwind_1d(x, F):
        """First-order accurate, unconditionally stable, non-conservative upwind advection scheme.
        """
        y = np.zeros_like(x)
        for i in range(1, x.shape[0]-1):
            y[i] = x[i+1]*(-np.minimum(F[0,i],0))\
                 + x[i-1]*(np.maximum(F[1,i],0))\
                 + x[i]*(np.minimum(F[0,i],0)-np.maximum(F[1,i],0))
        return y

class Diffusion:
    """Various schemes for discretising the diffusion term.
    """
    @nb.njit
    def central_difference_1d(x, D):
        """Second-order accurate central diffence scheme.
        """
        y = np.zeros_like(x)
        for i in range(1, x.shape[0]-1):
            y[i] = x[i-1]*D[0,i] + x[i+1]*D[1,i]\
                 - x[i]*(D[0,i]+D[1,i])
        return y

    # @nb.njit
    # def central_difference_2d(x, D0_0, D0_1, D1_0, D1_1):
    #     """Second-order accurate central diffence scheme.
    #     """
    #     y = np.zeros_like(x)
    #     for i in range(1,x.shape[0]-1):
    #         for j in range(1,x.shape[1]-1):
    #             y[i,j] = x[i-1,j]*D0_0[i,j] + x[i+1,j]*D0_1[i,j]\
    #                    + x[i,j-1]*D1_0[i,j] + x[i,j+1]*D1_1[i,j]\
    #                    - x[i,j]*(D0_0[i,j]+D0_1[i,j]+D1_0[i,j]+D1_1[i,j])
    #     return y