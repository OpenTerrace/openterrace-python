import numpy as np
import numba as nb
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