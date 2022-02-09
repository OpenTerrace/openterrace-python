import numpy as np
import solvers

class Tank:
    """This class handles modelling of the fluid phase in the storage tank.
        """
    def __init__(self, params, fluid):
        self.params = params
        self.fluid = fluid
        self.dy = params.h_tank/(params.ny_tank)
        self.y = np.linspace(0,params.h_tank,params.ny_tank+1)
        self.yc = 0.5*(self.y[:-1]+self.y[1:])
        self.V = self.dy*np.pi*(params.d_tank/2)**2
        self.bedCoupling = 1

    def select_schemes(self, conv=None, diff=None):
        """Imports the specified convection and diffusion schemes from the available schemes in schemes.py.
        """
        module = __import__('schemes')
        try:
            self.conv = getattr(module.Convection, conv)
        except:
            raise Exception('Valid convection schemes are: '+str([method for method in dir(module.Convection) if method.startswith('__') is False]))
        try:
            self.diff = getattr(module.Diffusion, diff)
        except:
            raise Exception('Valid diffusion schemes are: '+str([method for method in dir(module.Diffusion) if method.startswith('__') is False]))

    def apply_bcs(self):
        """Ensures a zero gradient, e.g. dT/dy=0, at the top of the tank
        """
        self.fluid.T[-1] = self.fluid.T[-2]

    def advance_time(self):
        LHS = self.conv(self.fluid.mdot*self.fluid.cp, self.fluid.T)\
            + self.diff(self.fluid.k/self.dy**2, self.fluid.T)\
            + self.bedCoupling
        print(self.conv(self.fluid.mdot*self.fluid.cp, self.fluid.T))
        dT_dt = LHS/(self.V*self.fluid.rho[1:-1]*self.fluid.cp[1:-1])
        self.fluid.T[1:-1] = self.fluid.T[1:-1] + dT_dt*self.params.dt

class Particle:
    """This class handles modelling of the particle phase.
        """
    def __init__(self, params, particle):
        self.params = params
        self.particle = particle
        self.dr = (params.d_particle/2)/(params.nx_particle-1)
        self.r = np.linspace(0, params.d_particle/2, params.nx_particle)
        self.r_faces = np.vstack(np.concatenate(([0], np.arange(self.dr/2,params.d_particle/2,self.dr).transpose(), [params.d_particle/2])))
        self.A_faces = particle.shape.area(self.r_faces)
        self.V_elements = particle.shape.vol_element(self.r_faces)

    def A_assembly(self):
        a1 = self.particle.k*self.A_faces[:-1]/self.dr
        a2 = -self.particle.k*self.A_faces[:-1]/self.dr - self.particle.k*self.A_faces[1:]/self.dr - self.particle.rho*self.particle.cp*self.V_elements/self.params.dt
        a3 = self.particle.k*self.A_faces[1:]/self.dr
        self.A = np.stack((a1, a2, a3), axis=0)
        self.A[-1,-1] = 0
        self.A[-2,-1] = -self.particle.k[-1]*self.A_faces[-2]/self.dr - self.particle.h*self.A_faces[-1] - self.particle.rho[-1]*self.particle.cp[-1]*self.V_elements[-1]/self.params.dt

    def b_assembly(self, Tfluid):
        self.b = -self.particle.T*self.particle.rho*self.particle.cp*self.V_elements/self.params.dt
        self.b[-1] -= self.particle.h*self.A_faces[-1]*Tfluid[1:-1,0]