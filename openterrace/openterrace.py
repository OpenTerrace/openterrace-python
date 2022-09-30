# Import Open Terrace modules
import fluids
import bedmaterials
import domains
import diffusion_schemes
import convection_schemes

# Import common Python modules
import tqdm
import numpy as np
import matplotlib.pyplot as plt
import sys

class OpenTerrace:
    def __init__(self, t_end=3600, dt=1):
        """Initialise Open Terrace with control parameters"""
        self.t = 0
        self.t_end = t_end
        self.dt = dt
        self.fluid = self.Phase(options='fluids')
        self.bed = self.Phase(options='bedmaterials')

    class Phase:
        def __init__(self, options):
            self.options = options

        def select_substance(self, substance=None):
            if not substance:
                raise Exception("Keyword 'substance' not specified.")
            if not substance in globals()[self.options].__all__:
                raise Exception("Substance "+substance+" specified. Valid fluid substances are:", globals()[self.options].__all__)
            self.fcns = getattr(globals()[self.options], substance)

        def select_domain(self, domain=None, **kwargs):
            """Select domain shape and type and initialise constants"""
            if not domain:
                raise Exception("Keyword 'domain' not specified.")
            if not domain in globals()['domains'].__all__:
                raise Exception("domain \'"+domain+"\' specified. Valid options for domain are:", domains.__all__)
            self.domain = getattr(globals()['domains'], domain)
            self.domain.validate_input(kwargs, domain)
            self.domain.shape = self.domain.shape(kwargs)
            self.domain.dx = self.domain.dx(kwargs)
            self.domain.A = self.domain.A(kwargs)
            self.domain.V = self.domain.V(kwargs)

        def select_scheme(self, diff=None, conv=None):
            """Imports the specified diffusion and convection schemes."""
            if diff:
                try:
                    self.diff = getattr(globals()['diffusion_schemes'], diff)
                except:
                    raise Exception("Diffusion scheme \'"+diff+"\' specified. Valid options for diffusion schemes are:", diffusion_schemes.__all__)
            else:
                self.diff = None

            if conv:
                try:
                    self.conv = getattr(globals()['convection_schemes'], conv)
                except:
                    raise Exception("Convection scheme \'"+conv+"\' specified. Valid options for convection schemes are:", convection_schemes.__all__)
            else:
                self.conv = None

        def initialise(self, T=None, mdot=None):
            """Initialises temperature and massflow fields"""
            if T:
                self.T = np.tile(T,(self.domain.shape+2))
                self.h = self.fcns.h(self.T)
            if mdot:
                self.mdot = (np.repeat(mdot, self.domain.shape+2), np.repeat(mdot, self.domain.shape+2))

        def update_properties(self):
            """Updates properties based on specific enthalpy"""
            self.T = self.fcns.T(self.h)
            self.rho = self.fcns.rho(self.h)
            self.cp = self.fcns.cp(self.h)
            self.k = self.fcns.k(self.h)
            if self.diff:
                self.D = self.k*self.domain.A/self.domain.dx
            if self.conv:
                self.F = self.mdot*self.cp

        def update_bc(self, bc_type=None, parameter=None, position=None, value=None):
            """Specify a boundary condition of type Neumann (specified gradient) or Dirichlet (specified value)"""
            valid_bc_types = ['neumann','dirichlet']
            if bc_type not in valid_bc_types:
                raise Exception("bc_type \'"+bc_type+"\' specified. Valid options for bc_type are:", valid_bc_types)
            valid_parameters = ['T','mdot']
            if parameter not in valid_parameters:
                raise Exception("parameter \'"+parameter+"\' specified. Valid options for parameter are:", valid_parameters)
            if not position:
                raise Exception("Keyword 'position' not specified.")
            if not value:
                raise Exception("Keyword 'value' not specified.")

        def advance_time(self):
            print(dir(self.diff))


    def run_simulation(self):
        """This is the function full of magic."""
        pass
        #for i in tqdm.tqdm(np.arange(0, self.t_end, self.dt)):
            

    def phase_coupling(self):
        pass

if __name__ == '__main__':
    ot = OpenTerrace(t_end=7200, dt=0.1)

    ot.fluid.select_substance(substance='air')
    ot.fluid.select_domain(domain='1d_cylinder', D=0.3, H=5, n=5)
    ot.fluid.select_scheme(diff='central_difference_1d', conv='upwind_1d')
    ot.fluid.initialise(T=300, mdot=0.01)
    ot.fluid.update_properties()
    # ot.fluid.update_bc(bc_type='dirichlet', parameter='T', position=(0, 0), value=400)
    ot.fluid.T[0] = 800

    # ot.bed.select_substance(substance='swedish_diabase')
    # ot.bed.select_domain(domain='1d_sphere', n=5, D=0.01)
    # ot.bed.select_scheme(diff='central_difference_1d')
   
    ot.fluid.advance_time()