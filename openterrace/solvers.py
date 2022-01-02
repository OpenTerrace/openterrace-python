import numpy as np
from scipy.linalg import solve_banded
from scipy.optimize import least_squares

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
    def __init__(self, const):
        self.dr = (const.d_p/2)/(const.nx_particles-1)
        self.r = np.linspace(0, const.d_p/2, const.nx_particles)
        self.rFace = np.concatenate(([0], np.arange(self.dr/2,const.d_p/2,self.dr), [const.d_p/2]))

    def matrix_assembly_tri(self, solid, particle):
        a1 = (self.solid.k*self.area/self.dr)[:-1]
        a2 = -self.solid.k*self.area[:-1]/self.dr - self.solid.k*self.area[1:]/self.dr - self.solid.rho*self.solid.cp*self.vol/self.params.dt
        a3 = (self.solid.k*self.area/self.dr)[1:]
        self.A0 = np.stack((a1, a2, a3), axis=0)

    def update_bc(self, **kwargs):
        self.bc_particle = kwargs['bc_particle']
        if self.bc_particle == 'forced_convection':
            if not 'h' in kwargs:
                raise Exception("Please specify 'h'")
            self.h = kwargs['h']
            self.A = self.A0

            self.A[-1,-1] = 0
            self.A[-2,-1] = -self.solid.k*self.area[-2]/self.dr - self.h*self.area[-1] - self.solid.rho*self.solid.cp*self.vol[-1]/self.params.dt

        else:
            raise Exception("Specify boundary condition on particle. Valid bc types are 'forced_convection'")

    def matrix_solve_tri(self, **kwargs):
        T_m0 = kwargs['T_m0']
        T_f0 = kwargs['T_f0']
        b = -T_m0*self.solid.rho*self.solid.cp*self.vol/self.params.dt

        if self.bc_particle == 'forced_convection':
            try:
                b[-1] -= self.h*self.area[-1]*kwargs['T_f0']
            except:
                raise Exception("Specify T_f0")

        return solve_banded((1, 1), self.A, b)

    def analytical(self, n_terms=15):
        def func(lambda_n):
            Bi = self.h*(self.params.dp/2)/self.solid.k
            return 1-lambda_n*np.cos(lambda_n)/np.sin(lambda_n)-Bi
        
        Fo = self.solid.k/(self.solid.rho*self.solid.cp) * self.params.t_end / (self.params.dp/2)**2

        arr_lambda_n = np.array([])
        i = 1
        while len(arr_lambda_n) < n_terms:
            lambda_n = float("%0.6f" % least_squares(func, i, bounds = (1, np.inf)).x)

            if lambda_n not in arr_lambda_n:
                arr_lambda_n = np.append( arr_lambda_n , lambda_n)
            i += 0.1

        self.theta = []
        for r in self.r:
            self.theta = np.append(self.theta, (np.sum(4*(np.sin(arr_lambda_n)-arr_lambda_n*np.cos(arr_lambda_n))/(2*arr_lambda_n-np.sin(2*arr_lambda_n)) * np.exp(-arr_lambda_n**2*Fo) * np.sin(arr_lambda_n*r/(self.params.dp/2))/(arr_lambda_n*r/(self.params.dp/2)))))