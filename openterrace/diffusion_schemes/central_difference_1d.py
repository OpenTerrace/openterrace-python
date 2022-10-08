import numpy as np
import numba as nb

@nb.njit
def central_difference_1d(x, D):
    """Second-order accurate central diffence scheme.
    """
    _out = np.zeros_like(x)
    for i in range(1, x.shape[0]-1):
        _out[i] = x[i-1]*D[0,i] + x[i+1]*D[1,i]\
            - x[i]*(D[0,i]+D[1,i])
    return _out