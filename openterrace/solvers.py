import numpy as np

class Tank:
    """This class handles modelling of the fluid phase in the storage tank.
        """
    def __init__(self, params, fluid):
        self.params = params
        self.fluid = fluid
        self.dy = params.h_tank/(params.ny_tank)
        self.y = np.linspace(0,params.h_tank,params.ny_tank+1)
        self.yc = 0.5*(self.y[:-1]+self.y[1:])

    def select_schemes(self, conv=None, diff=None):
        module = __import__('schemes')
        try:
            self.conv = getattr(module.Convective, conv)
        except:
            raise Exception('Valid convection schemes are: '+str([method for method in dir(module.Convective) if method.startswith('__') is False]))
        try:
            self.diff = getattr(module.Diffusion, diff)
        except:
            raise Exception('Valid diffusion schemes are: '+str([method for method in dir(module.Diffusion) if method.startswith('__') is False]))

    def eq(self):
#       LHS = self.conv(self.fluid.u*self.fluid.rho*self.fluid.cp/self.dy,self.fluid.T)\
#            + self.diff(self.fluid.k/self.dy**2,self.fluid.T)
        LHS = self.conv(self.fluid.u*self.fluid.rho*self.fluid.cp/self.dy,self.fluid.T)

        self.fluid.T[1:-1] += LHS*self.params.dt/(self.fluid.rho[1:-1]*self.fluid.cp[1:-1])

    def update_lower_bc(self):
        self.fluid.T[0] = self.params.update_inlet_temperature(self.params.t)
    
    def update_upper_bc(self):
        self.fluid.T[-2] = self.fluid.T[-1]

class Particle:
    """This class handles modelling of the particle phase.
        """
    def __init__(self, params, particle):
        self.params = params
        self.particle = particle
        self.dr = (params.dp_particle/2)/(params.nx_particle-1)
        self.r = np.linspace(0, params.dp_particle/2, params.nx_particle)
        self.r_faces = np.vstack(np.concatenate(([0], np.arange(self.dr/2,params.dp_particle/2,self.dr).transpose(), [params.dp_particle/2])))
        self.A_faces = particle.shape.area(self.r_faces)
        self.V_elements = particle.shape.vol_element(self.r_faces)