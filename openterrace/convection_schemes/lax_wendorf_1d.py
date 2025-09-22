import numpy as np
import numba as nb

@nb.njit
def lax_wendorf_1d(x, F):
    """Second-order accurate, conditionally stable, conservative Lax-Wendroff advection scheme.
    """
    _out = np.zeros_like(x)
    for j in range(1, x.shape[0]-1):
        for i in range(0, x.shape[1]):
            _out[j,i] = x[j,i] - 0.5 * F[0,j,i] * (x[j+1,i] - x[j-1,i]) + 0.5 * F[0,j,i]**2 * (x[j+1,i] - 2*x[j,i] + x[j-1,i])
    return _out