import numpy as np

def tridiagonal(A, b):
    """Solves n sets of Ax=b systems for x, where A is tridiagonal.
        Args:
            A ndarray: 3D array containing data with `float` type. Upper diagonal, diagonal, lower diagonal, in same format as scipy.linalg.solve_banded
            b ndarray: 2D array containing data with `float` type.
        Returns:
            ndarray: 2D array containing data with `float` type.
        Example:
            Solves two 3x3 Ax=b systems with ones at the diagonal and zeros on upper and lower diagonal
            >>> A=[[[0,0,0],[0,0,0]],[[1,1,1],[1,1,1]],[[0,0,0],[0,0,0]]]
            >>> b=[[1,1,1],[1,1,1]]
            >>> solve_tridiagonal(A, b)
            [[1,1,1],[1,1,1]]]
    """
    b_ = b.copy()
    x = np.zeros_like(b)
    n = b.shape[0]
    a0, a1, a2 = A.copy()
    for i in range(1, n):
        w = a2[i-1] / a1[i-1]
        a1[i] -= w * a0[i]
        b_[i] -= w * b_[i-1]
    x[-1] = b_[-1] / a1[-1]
    for i in range(n-1)[::-1]:
        x[i] = (b_[i] - a0[i+1] * x[i + 1]) / a1[i]
    return x