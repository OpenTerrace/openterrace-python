# Import OpenTerrace modules
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
    def __init__(self, t_end=3600, dt=1, n_fluid=None, n_bed=None):
        """Initialise OpenTerrace with control parameters"""
        self.t = 0
        self.t_end = t_end
        self.dt = dt
        self.fluid = self.Phase(n_fluid, _type='fluid', options='fluids')
        self.bed = self.Phase(n_bed, _type='bed', options='bedmaterials')

    class Phase:
        def __init__(self, n, _type, options):
            self.n = n
            self._type = _type
            self.options = options
            self._bcs = []

        def select_substance(self, substance=None):
            if not substance:
                raise Exception("Keyword 'substance' not specified.")
            if not substance in globals()[self.options].__all__:
                raise Exception(substance+" specified as "+self._type+" substance. Valid "+self._type+" substances are:", globals()[self.options].__all__)
            self.fcns = getattr(globals()[self.options], substance)

        def select_domain(self, domain=None, **kwargs):
            """Select domain shape and type and initialise constants"""
            kwargs['n'] = self.n
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
                    self.diff = getattr(getattr(globals()['diffusion_schemes'], diff), diff)
                except:
                    raise Exception("Diffusion scheme \'"+diff+"\' specified. Valid options for diffusion schemes are:", diffusion_schemes.__all__)
            else:
                self.diff = None

            if conv:
                try:
                    self.conv = getattr(getattr(globals()['convection_schemes'], conv), conv)
                except:
                    raise Exception("Convection scheme \'"+conv+"\' specified. Valid options for convection schemes are:", convection_schemes.__all__)
            else:
                self.conv = None

        def initialise(self, T=None, mdot=None, nFluidPhase=1):
            """Initialises temperature and massflow fields"""
            if T:
                self.T = np.tile(T,(np.append(self.domain.shape+2,nFluidPhase)))
                self.h = self.fcns.h(self.T)
            if mdot:
                self.mdot = np.tile(mdot,(np.append(self.domain.shape+2,nFluidPhase)))
                #self.mdot = np.repeat(mdot, self.domain.shape+2), np.repeat(mdot, self.domain.shape+2)

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

        def define_bc(self, bc_type=None, parameter=None, position=None, value=None):
            """Specify a boundary condition of type Neumann (specified gradient) or Dirichlet (specified value)"""
            valid_bc_types = ['neumann','dirichlet','robin']
            if bc_type not in valid_bc_types:
                raise Exception("bc_type \'"+bc_type+"\' specified. Valid options for bc_type are:", valid_bc_types)
            valid_parameters = ['T','mdot']
            if parameter not in valid_parameters:
                raise Exception("parameter \'"+parameter+"\' specified. Valid options for parameter are:", valid_parameters)
            if not position:
                raise Exception("Keyword 'position' not specified.")
            if not value and bc_type=='dirichlet':
                raise Exception("Keyword 'value' is needed for dirichlet type bc.")
            self._bcs.append({'type': bc_type, 'parameter': parameter, 'position': position, 'value': value})

        def enforce_bcs(self):
            for bc in self._bcs:
                if bc['type'] == 'dirichlet':
                    self.h[bc['position'][1]] = self.fcns.h(bc['value'])
                if bc['type'] == 'neumann':
                    if bc['position'][1] == 0:
                        self.h[0] = self.h[1]
                    if bc['position'][1] == 1:
                        self.h[-1] = self.h[-2]
                if bc['type'] == 'robin':
                    pass

        def solve_equations(self, dt):
            if self.diff:
                self.h = self.h - self.diff(self.T, self.D)/(self.rho*self.domain.V)*dt
            if self.conv:
                self.h = self.h + self.conv(self.T, self.F)/(self.rho*self.domain.V)*dt

    def run_simulation(self):
        """This is the function full of magic."""
        _arr_out = np.zeros_like(self.fluid.T)
        for i in tqdm.tqdm(np.arange(0, self.t_end, self.dt)):
            self.fluid.solve_equations(self.dt)
            self.fluid.enforce_bcs()
            self.fluid.update_properties()
        
    def phase_coupling(self):
        pass

if __name__ == '__main__':
    ot = OpenTerrace(t_end=1800, dt=0.1, n_fluid=10, n_bed=5)

    ot.fluid.select_substance(substance='water')
    ot.fluid.select_domain(domain='1d_cylinder', D=1, H=5)
    ot.fluid.select_scheme(conv='upwind_1d') #diff='central_difference_1d')
    ot.fluid.initialise(T=20+273.15, mdot=1)
    ot.fluid.define_bc(bc_type='dirichlet', parameter='T', position=(0,0), value=80+273.15)
    ot.fluid.define_bc(bc_type='neumann', parameter='T', position=(0,1))
    ot.fluid.update_properties()

    # ot.bed.select_substance(substance='magnetite')
    # ot.bed.select_domain(domain='1d_sphere', D=0.05, n=7)
    # ot.bed.select_scheme(diff='central_difference_1d')
    # ot.bed.initialise(T=50+273.15)
    # ot.bed.define_bc(bc_type='neumann', parameter='T', position=(0,0))
    # ot.bed.define_bc(bc_type='neumann', parameter='T', position=(0,1))
    # ot.bed.update_properties()

    # ot.run_simulation()

    # ot.bed.select_substance(substance='swedish_diabase')
    # ot.bed.select_domain(domain='1d_sphere', n=5, D=0.01)
    # ot.bed.select_scheme(diff='central_difference_1d')