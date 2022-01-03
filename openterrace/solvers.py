import numpy as np
from scipy.linalg import solve_banded
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

class ConvDiff1D:
    def __init__(self, u, alpha, yStart, yEnd, ny, dt):
        self.u = u
        self.alpha = alpha
        self.yStart = yStart  
        self.yEnd = yEnd
        self.ny = ny
        self.dt = dt   
        self.dy = (yEnd-yStart)/ny

    def matrix_assembly(self, scheme):
        if scheme == 'upwind':
            a1 = [ self.alpha*self.dt/self.dy**2.0     + max(self.u*self.dt/self.dy,0)] * (self.ny-1)
            a2 = [-2.0*self.alpha*self.dt/self.dy**2.0 + 1 + min(self.u*self.dt/self.dy,0) - max(self.u*self.dt/self.dy,0) ] * (self.ny)
            a3 = [ self.alpha*self.dt/self.dy**2.0     - min(self.u*self.dt/self.dy,0)] * (self.ny-1)
            self.A = np.diag(a1, -1) + np.diag(a2, 0) + np.diag(a3, 1)

        elif scheme == "centralDifference":
            a1 = [ self.alpha*self.dt/self.dy**2.0     + self.u*self.dt/(2*self.dy)] * (self.ny-1)
            a2 = [-2.0*self.alpha*self.dt/self.dy**2.0 + 1] * (self.ny)
            a3 = [ self.alpha*self.dt/self.dy**2.0     - self.u*self.dt/(2*self.dy)] * (self.ny-1)
            self.A = np.diag(a1, -1) + np.diag(a2, 0) + np.diag(a3, 1)
        else:
            raise Exception("Valid schemes are 'upwind' and 'centralDifference'")
    
    def MatrixSolve(self, T0):
        return np.matmul(self.A, T0)

class Diff1D():
    def __init__(self, const, prop):
        self.dr = (const.d_p/2)/(const.nx_particles-1)
        self.r = np.linspace(0, const.d_p/2, const.nx_particles)
        self.r_faces = np.vstack(np.concatenate(([0], np.arange(self.dr/2,const.d_p/2,self.dr).transpose(), [const.d_p/2])))
        self.A_faces = prop.shape.area(self.r_faces)
        self.V_elements = prop.shape.vol_element(self.r_faces)

    def matrix_assembly_tri(self, const, particle):
        a1 = particle.k*self.A_faces[:-1]/self.dr
        a2 = -particle.k*self.A_faces[:-1]/self.dr - particle.k*self.A_faces[1:]/self.dr - particle.rho*particle.cp*self.V_elements/const.dt
        a3 = particle.k*self.A_faces[1:]/self.dr
        return np.stack((a1, a2, a3), axis=0)

    def update_A(self, const, particle, A0):
        A0[-1,-1] = 0
        A0[-2,-1] = -particle.k[-1]*self.A_faces[-2]/self.dr - particle.h*self.A_faces[-1] - particle.rho[-1]*particle.cp[-1]*self.V_elements[-1]/const.dt
        return A0

    def update_b(self, const, particle, fluid, Tm0):
        b = -Tm0*particle.rho*particle.cp*self.V_elements/const.dt
        b[-1] -= particle.h*self.A_faces[-1]*fluid.T_old
        return b

    def solve_tridiagonal(self, A, b):
        """
        Solve Ax=b for x, where A is tridiagonal.
            
        :param A: Upper diagonal, diagonal, lower diagonal, in same format as solve_banded
        :param b: right hand side
        :return: x=A^{-1}b
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

    def analytical(self, const, particle, n_terms=5):
        def func(lambda_n):
            Bi = particle.h[0]*(const.d_p/2)/particle.k[0,0]
            return 1-lambda_n*np.cos(lambda_n)/np.sin(lambda_n)-Bi
        
        Fo = particle.k[0,0]/(particle.rho[0,0]*particle.cp[0,0]) * const.t_end / (const.d_p/2)**2

        arr_lambda_n = np.array([])
        i = 0.1
        while len(arr_lambda_n) < n_terms:
            lambda_n = float("%0.6f" % least_squares(func, i, bounds = (0.1, np.inf)).x)

            if lambda_n not in arr_lambda_n:
                arr_lambda_n = np.append(arr_lambda_n ,lambda_n)
            i += 0.01

        Bi = particle.h[0]*(const.d_p/2)/particle.k[0,0]
        lambda_n = np.linspace(0,45,200)
        y = 1-lambda_n*np.cos(lambda_n)/np.sin(lambda_n)-Bi
        
        self.theta = []
        for r in self.r:
            self.theta = np.append(self.theta, (np.sum(4*(np.sin(arr_lambda_n)-arr_lambda_n*np.cos(arr_lambda_n))/(2*arr_lambda_n-np.sin(2*arr_lambda_n)) * np.exp(-arr_lambda_n**2*Fo) * np.sin(arr_lambda_n*r/(const.d_p/2))/(arr_lambda_n*r/(const.d_p/2)))))