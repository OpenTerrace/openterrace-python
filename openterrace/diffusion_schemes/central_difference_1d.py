import numpy as np
import numba as nb
from numba import cuda

# @nb.njit
# def central_difference_1d(x, D):
#     """Second-order accurate central diffence scheme.
#     """
#     _out = np.zeros_like(x)
#     for j in range(0, x.shape[0]):
#         for i in range(1, x.shape[1]-1):
#             _out[j,i] = x[j,i-1]*D[0,j,i] + x[j,i+1]*D[1,j,i]\
#                 - x[j,i]*(D[0,j,i]+D[1,j,i])
#             # _out[j,i] = x[j,i-1]*D[0,j,i] + x[j,i+1]*D[1,j,i]\
#             #     - x[j,i]*(D[0,j,i]+D[1,j,i])                
#     return _out

@cuda.jit
def central_difference_1d(x, D):
    """Second-order accurate central diffence scheme.
    """
    _out = np.zeros_like(x)
    j,i = cuda.grid(2)
    if j < x.shape[0] and i < x.shape[1]-1:
        _out[j,i] = x[j,i-1]*D[0,j,i] + x[j,i+1]*D[1,j,i]\
            - x[j,i]*(D[0,j,i]+D[1,j,i])     
    return _out
