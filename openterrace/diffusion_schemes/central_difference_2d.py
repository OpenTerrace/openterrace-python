import numpy as np
import numba as nb

@nb.njit
def central_difference_2d(x, D):
    """Second-order accurate central diffence scheme.
    """
    y = np.zeros_like(x)
    for i in range(1,x.shape[0]-1):
        for j in range(1,x.shape[1]-1):
            y[i,j] = x[i-1,j]*D0_0[i,j] + x[i+1,j]*D0_1[i,j]\
                + x[i,j-1]*D1_0[i,j] + x[i,j+1]*D1_1[i,j]\
                - x[i,j]*(D0_0[i,j]+D0_1[i,j]+D1_0[i,j]+D1_1[i,j])
    return y