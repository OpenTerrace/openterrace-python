import numpy as np
import numba as nb

class Convection:
    """Various schemes for discretising the advection term.
    """
    @nb.njit
    def upwind(x, Fw, Fe, Fn, Fs, y):
        """First-order accurate, unconditionally stable, non-conservative upwind advection scheme.
        """
        for i in range(1,x.shape[0]-1):
            for j in range(1,x.shape[1]-1):
                y[i,j] = x[i+1,j]*(-np.minimum(Fs[i,j],0))\
                       + x[i-1,j]*(np.maximum(Fn[i,j],0))\
                       + x[i,j]*(np.minimum(Fs[i,j],0)-np.maximum(Fn[i,j],0))
        return y

class Diffusion:
    """Various schemes for discretising the diffusion term.
    """
    @nb.njit
    def central_difference_2d(x, Dw, De, Dn, Ds, y):
        """Second-order accurate central diffence scheme.
        """
        for i in range(1,x.shape[0]-1):
            for j in range(1,x.shape[1]-1):
                y[i,j] = x[i,j-1]*Dw[i,j] + x[i,j+1]*De[i,j]\
                       + x[i+1,j]*Ds[i,j] + x[i-1,j]*Dn[i,j]\
                       - x[i,j]*(Dw[i,j]+De[i,j]+Ds[i,j]+Dn[i,j])
        return y

    @nb.njit
    def central_difference_1d(x, Dw, De, Dn, Ds, y):
        """Second-order accurate central diffence scheme.
        """
        for i in range(1,x.shape[0]-1):
            for j in range(1,x.shape[1]-1):
                y[i,j] = x[i,j-1]*Dw[i,j] + x[i,j+1]*De[i,j]\
                       + x[i+1,j]*Ds[i,j] + x[i-1,j]*Dn[i,j]\
                       - x[i,j]*(Dw[i,j]+De[i,j]+Ds[i,j]+Dn[i,j])
        return y