import numpy as np
import timeit


def solve_tridiagonal(A, y):
    """
    Solve Ax=y for x, where A is tridiagonal.
    
    :param A: Upper diagonal, diagonal, lower diagonal, in same format as solve_banded
    :param y: right hand side
    :return: x=A^{-1}y
    """
    y_ = y.copy()
    x = np.zeros_like(y)
    n = y.shape[0]
    a0, a1, a2 = A.copy()
    for i in range(1, n):
        w = a2[i-1] / a1[i-1]
        a1[i] -= w * a0[i]
        y_[i] -= w * y_[i-1]
    x[-1] = y_[-1] / a1[-1]
    for i in range(n-1)[::-1]:
        x[i] = (y_[i] - a0[i+1] * x[i + 1]) / a1[i]
    return x


if __name__ == '__main__':
    m = 3
    n = 2
    bands = np.tile(
        np.array([
            np.zeros(n),
            np.ones(n),
            np.zeros(n),
        ])[..., None],
        [1, 1, m]
    )
    rhs = np.ones((n, m))

    print(bands)
    print(rhs)
    
    tic0 = timeit.default_timer()
    x = solve_tridiagonal(bands, rhs)
    print(x)
    tic1 = timeit.default_timer()
    print(tic1 - tic0)

    x = np.zeros_like(rhs)
    for i in range(m):
        x[:, i] = solve_tridiagonal(bands[..., i], rhs[:, i])
    tic2 = timeit.default_timer()
    print(tic2 - tic1)