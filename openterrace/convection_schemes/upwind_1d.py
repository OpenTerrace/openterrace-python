import numpy as np
import numba as nb

@nb.njit
def upwind_1d(x, F):
    """First-order accurate, unconditionally stable, non-conservative upwind advection scheme.
    """
    _out = np.zeros_like(x)
    for j in range(1, x.shape[0]-1):
        for i in range(0, x.shape[1]):
            _out[j,i] = x[j+1,i]*(-np.minimum(F[0,j,i],0))\
                + x[j-1,i]*(np.maximum(F[1,j,i],0))\
                + x[j,i]*(np.minimum(F[0,j,i],0)-np.maximum(F[1,j,i],0))
    return _out