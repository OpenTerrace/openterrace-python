# Open Terrace modules
import fluids
import bedmaterials
import domains
import schemes

# Common Python modules
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import sys

class OpenTerrace:
    def __init__(self, t_end=3600, dt=1):
        """Initialise Open Terrace with control parameters"""
        self.t = 0
        self.t_end = t_end
        self.dt = dt
    
    def define_fluid_phase(self, substance=None):
        """Load functions for the fluid phase"""
        if not substance:
            raise Exception("Keyword 'substance' not specified.")
        if not substance in globals()['fluids'].__all__:
            raise Exception("Substance "+substance+" specified. Valid fluid substances are:", globals()['fluids'].__all__)
        self.fluid = getattr(globals()['fluids'], substance)
    
    def define_bed_phase(self, substance=None):
        """Load functions for the bed phase"""
        if not substance:
            raise Exception("Keyword 'substance' not specified.")
        if not substance in globals()['bedmaterials'].__all__:
            raise Exception("Substance "+substance+" specified. Valid bed material substances are:", globals()['bedmaterials'].__all__)
        self.bed = getattr(globals()['bedmaterials'], substance) 
    
    def select_fluid_domain(self, domain=None, **kwargs):
        """Select domain shape and type and initialise constants"""
        if not domain:
            raise Exception("Keyword 'domain' not specified.")
        if not domain in globals()['domains'].__all__:
            raise Exception("domain \'"+domain+"\' specified. Valid options for domain are:", domains.__all__)
        self.fluid.domain = getattr(globals()['domains'], domain)
        self.fluid.domain.validate_input(kwargs, domain)
        self.fluid.domain.shape = self.fluid.domain.shape(kwargs)
        self.fluid.domain.A = self.fluid.domain.A(kwargs)
        self.fluid.domain.V = self.fluid.domain.V(kwargs)

    def select_bed_domain(self, domain=None, **kwargs):
        """Select domain shape and type and initialise constants"""
        if not domain:
            raise Exception("Keyword 'domain' not specified.")
        if not domain in globals()['domains'].__all__:
            raise Exception("domain \'"+domain+"\' specified. Valid options for domain are:", domains.__all__)
        self.bed.domain = getattr(globals()['domains'], domain)
        self.bed.domain.validate_input(kwargs, domain)
        self.bed.domain.shape = self.bed.domain.shape(kwargs)
        self.bed.domain.A = self.bed.domain.A(kwargs)
        self.bed.domain.V = self.bed.domain.V(kwargs)

    def select_bed_schemes(self, diff=None):
        """Imports the specified diffusion scheme from the available schemes in schemes.py.
        """
        if diff:
            try:
                self.bed.diff = getattr(schemes.Diffusion, diff)
            except:
                raise Exception('Valid diffusion schemes are: '+str([method for method in dir(schemes.Diffusion) if method.startswith('__') is False]))
        else:
            self.bed.diff = diff

    def select_fluid_schemes(self, diff=None, conv=None):
        """Imports the specified diffusion and convection schemes from the available schemes in schemes.py.
        """
        if diff:
            try:
                self.fluid.diff = getattr(schemes.Diffusion, diff)
            except:
                raise Exception('Valid diffusion schemes are: '+str([method for method in dir(schemes.Diffusion) if method.startswith('__') is False]))
        else:
            self.fluid.diff = diff
        
        if conv:
            try:
                self.fluid.conv = getattr(schemes.Convection, conv)
            except:
                raise Exception('Valid convection schemes are: '+str([method for method in dir(schemes.Convection) if method.startswith('__') is False]))
        else:
            self.fluid.conv = conv

    def set_initial_fields(self, Tf=None, Tb=None):
        if not Tf:
            raise Exception("Keyword 'Tf' not specified.")
        if not Tb:
            raise Exception("Keyword 'Tb' not specified.")
        self.fluid.T = np.tile(Tf,(self.fluid.domain.shape+2))
        self.bed.T = np.tile(Tb,(self.bed.domain.shape+2)) 

    def update_massflow(self):
        self.fluid.mdot = (np.repeat(0.01, self.fluid.domain.shape+2), np.repeat(0.01, self.fluid.domain.shape+2))

    def set_boundary_condition(self, phase=None, bc_type=None, parameter=None, position=None, value=None):
        """Specify a boundary condition of type Neumann (fixed value) or Dirichlet (fixed gradient)"""
        if not phase:
            raise Exception("Keyword 'phase' not specified. How should I know which phase you are trying to specify a boundary condition for?")
        if phase not in ['fluid','bed']:
            raise Exception("phase \'"+phase+"\' specified. Valid options for bc_type are:", phase)
        valid_bc_types = ['neumann']#,'dirichlet']
        if bc_type not in valid_bc_types:
            raise Exception("bc_type \'"+bc_type+"\' specified. Valid options for bc_type are:", valid_bc_types)
    
    def update_fluid_properties(self):
        self.fluid.rho = self.fluid.rho(self.fluid.T)
        self.fluid.cp = self.fluid.cp(self.fluid.T)
        self.fluid.k = self.fluid.k(self.fluid.T)

        self.fluid.D = self.fluid.domain.A*self.fluid.k
        self.fluid.F = self.fluid.mdot*self.fluid.cp

    def run_simulation(self):
        """This is the loop where all the magic happens."""
        _arr_out = np.zeros_like(self.fluid.T)

        for i in tqdm(np.arange(0, self.t_end, self.dt)):
            Qdot = np.zeros_like(self.fluid.T)
            if self.fluid.diff:
                Qdot += self.fluid.diff(self.fluid.T, self.fluid.D)
            if self.fluid.conv:
                Qdot += self.fluid.conv(self.fluid.T, self.fluid.F)

            self.fluid.T += Qdot*self.dt/(self.fluid.rho*self.fluid.domain.V*self.fluid.cp)

        plt.plot(self.fluid.T)
        plt.grid()
        plt.xlabel('Position y')
        plt.ylabel('Temperature T')
        plt.show()
        sys.exit()

if __name__ == '__main__':
    ot = OpenTerrace(t_end=7200, dt=0.01)
    
    ot.define_fluid_phase(substance='air')
    ot.define_bed_phase(substance='swedish_diabase')

    ot.select_fluid_domain(domain='1d_cylinder', D=0.3, H=5, n=5)
    ot.select_bed_domain(domain='1d_sphere', D=0.01, n=10)

    ot.select_fluid_schemes(conv='upwind_1d', diff='central_difference_1d')
    ot.select_bed_schemes(diff='central_difference_1d')

    ot.set_initial_fields(Tf=600+273.15, Tb=600+273.15)

    ot.set_boundary_condition(phase='fluid', bc_type='neumann', parameter='temperature', position=(0, 0), value=300)

    ot.update_massflow()
    ot.update_fluid_properties()

    ot.run_simulation()