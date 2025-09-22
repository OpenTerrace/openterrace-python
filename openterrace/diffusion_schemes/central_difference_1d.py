import numpy as np
import numba as nb

@nb.njit
def central_difference_1d(x, D):
    """Second-order accurate central diffence scheme.
    """
    _out = np.zeros_like(x)
    for j in range(1, x.shape[0]-1):
        for i in range(0, x.shape[1]):
            _out[j,i] = x[j-1,i]*D[0,j,i] + x[j+1,i]*D[1,j,i]\
                - x[j,i]*(D[0,j,i]+D[1,j,i])             
    return _out