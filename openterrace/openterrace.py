# Import OpenTerrace modules
import openterrace.fluid_substances
import bed_substances
import domains
import diffusion_schemes
import convection_schemes

# Import common Python modules
import tqdm
import numpy as np
import matplotlib.pyplot as plt
import sys

class OpenTerrace:
    """OpenTerrace class."""
    def __init__(self, t_end:float=3600, dt:float=1, n_fluid:float=1, n_bed:float=10):
        """Initialise with various control parameters.

        Args:
            t_end (float): End time in s
            dt (float): Time step size in s
            n_fluid (float): Number of discretisations for fluid phase
            n_bed (float): Number of discretisations for bed phase
        """
        self.t = 0
        self.t_end = t_end
        self.dt = dt
        self.fluid = self.Phase(n=n_fluid, _type='fluid', options='fluid_substances')
        self.bed = self.Phase(n=n_bed, n2=n_fluid, _type='bed', options='bed_substances')

    class Phase:
        """Main class to define to define either the fluid or bed phase."""
        def __init__(self, n=None, n2=1, _type=None, options=None):
            self.n = n
            self.n2 = n2
            self.options = options
            self._type = _type
            self._bcs = []
            self._sources = []

        def define_substance_on_the_fly(self, cp:float=None, rho:float=None, k:float=None, mu:float=None):
            """Defines a new substance on-the-fly. This is useful for defining a substance for testing purposes with temperature independent properties.

            Args:
                cp (float): Specific heat capacity in J/(kg K)
                rho (float): Density in kg/m^3
                k (float): Thermal conductivity in W/(m K)
                mu (float): Dynamic viscosity in kg/(m s)
            """
            class dummy:
                pass
            self.fcns = dummy()
            self.fcns.h = lambda T: np.ones_like(T)*T*cp
            self.fcns.T = lambda h: np.ones_like(h)*h/cp
            self.fcns.cp = lambda h: np.ones_like(h)*cp
            self.fcns.k = lambda h: np.ones_like(h)*k
            self.fcns.mu = lambda h: np.ones_like(h)*mu
            self.fcns.rho = lambda h: np.ones_like(h)*rho

        def select_substance(self, substance:str=None):
            """Selects one of the predefined substancers.

            Args:
                substance (str): Substance name
            """
            if not substance:
                raise Exception("Keyword 'substance' not specified.")
            if not substance in globals()[self.options].__all__:
                raise Exception(substance+" specified as "+self._type+" substance. Valid "+self._type+" substances are:", globals()[self.options].__all__)
            self.fcns = getattr(globals()[self.options], substance)

        def select_domain(self, domain:str=None, **kwargs):
            """Select domain shape and initialise constants."""
            kwargs['n'] = self.n
            if not domain:
                raise Exception("Keyword 'domain' not specified.")
            if not domain in globals()['domains'].__all__:
                raise Exception("domain \'"+domain+"\' specified. Valid options for domain are:", domains.__all__)
            self.domain = getattr(globals()['domains'], domain)
            self.domain.validate_input(kwargs, domain)
            self.domain.shape = self.domain.shape(kwargs)
            self.domain.node_pos = self.domain.node_pos(kwargs)
            self.domain.dx = self.domain.dx(kwargs)
            self.domain.A = self.domain.A(kwargs)
            self.domain.V = self.domain.V(kwargs)

        def select_schemes(self, diff=None, conv=None):
            """Imports the specified diffusion and convection schemes."""
            if diff is not None:
                try:
                    self.diff = getattr(getattr(globals()['diffusion_schemes'], diff), diff)
                except:
                    raise Exception("Diffusion scheme \'"+diff+"\' specified. Valid options for diffusion schemes are:", diffusion_schemes.__all__)
            else:
                self.diff = None

            if conv is not None:
                try:
                    self.conv = getattr(getattr(globals()['convection_schemes'], conv), conv)
                except:
                    raise Exception("Convection scheme \'"+conv+"\' specified. Valid options for convection schemes are:", convection_schemes.__all__)
            else:
                self.conv = None

        def initialise(self, T=None, mdot=None):
            """Initialises temperature and massflow fields"""
            if T is not None:
                self.T = np.tile(T,(np.append(self.n2,self.domain.shape)))
                self.h = self.fcns.h(self.T)
            if mdot is not None:
                self.mdot = np.tile(mdot,(np.append(self.n2,self.domain.shape)))

            self.T = self.fcns.T(self.h)
            self.rho = self.fcns.rho(self.h)
            self.cp = self.fcns.cp(self.h)
            self.k = self.fcns.k(self.h)

            self.D = np.zeros(((2,)+(self.T.shape)))
            self.F = np.zeros(((2,)+(self.T.shape)))
            self.S = np.zeros(self.T.shape)

        def update_properties(self):
            """Updates properties based on specific enthalpy"""
            self.T = self.fcns.T(self.h)
            self.rho = self.fcns.rho(self.h)
            self.cp = self.fcns.cp(self.h)
            self.k = self.fcns.k(self.h)

            if self.diff is not None:
                self.D[0,:,:] = self.k*self.domain.A[0]/self.domain.dx
                self.D[1,:,:] = self.k*self.domain.A[1]/self.domain.dx

            if self.conv is not None:
                self.F[0,:,:] = self.mdot*self.cp
                self.F[1,:,:] = self.mdot*self.cp

        def define_bc(self, bc_type=None, parameter=None, position=None, value=None):
            """Specify boundary condition type"""
            valid_bc_types = ['neumann','dirichlet']
            if bc_type not in valid_bc_types:
                raise Exception("bc_type \'"+bc_type+"\' specified. Valid options for bc_type are:", valid_bc_types)
            valid_parameters = ['T','mdot']
            if parameter not in valid_parameters:
                raise Exception("parameter \'"+parameter+"\' specified. Valid options for parameter are:", valid_parameters)
            if not position:
                raise Exception("Keyword 'position' not specified.")
            if value is None and bc_type=='dirichlet':
                raise Exception("Keyword 'value' is needed for dirichlet type bc.")
            self._bcs.append({'type': bc_type, 'parameter': parameter, 'position': position, 'value': value})

        def update_boundary_nodes(self, dt):
            """Update boundary nodes"""
            for bc in self._bcs:
                if bc['type'] == 'dirichlet':
                    self.h[bc['position']] = self.fcns.h(bc['value'])
                if bc['type'] == 'neumann':
                    if bc['position'] == np.s_[:,0]:
                        self.h[bc['position']] = self.h[bc['position']] + (2*self.T[:,1]*self.D[0,:,1] - 2*self.T[:,0]*self.D[1,:,0])/(self.rho[:,0]*self.domain.V[0])*dt
                    if bc['position'] == np.s_[:,-1]:
                        self.h[bc['position']] = self.h[bc['position']] + (2*self.T[:,-2]*self.D[0,:,-1] - 2*self.T[:,-1]*self.D[1,:,-1])/(self.rho[:,-1]*self.domain.V[-1])*dt

        def solve_equations(self, dt):
            if self.diff is not None:
                self.h = self.h + self.diff(self.T, self.D)/(self.rho*self.domain.V)*dt
            if self.conv is not None:
                self.h = self.h + self.conv(self.T, self.F)/(self.rho*self.domain.V)*dt

        def define_source_term(self, **kwargs):#source_type:str=None, h_type:str=None, h_coeff:float=None, slice=None):
            """Define source terms"""
            self._sources.append(kwargs)

    def add_source_terms(self):
        self.bed.h[bed_s] = self.bed.h[bed_s] + h_coeff*self.bed.domain.A[0,-1]*(self.fluid.T[fluid_s]-self.bed.T[bed_s])

    def run_simulation(self):
        """This is the function full of magic."""
        for i in tqdm.tqdm(np.arange(0, self.t_end, self.dt)):
            if hasattr(self.bed, 'T'):
                self.bed.solve_equations(self.dt)
                self.bed.update_properties()
                self.bed.update_boundary_nodes(self.dt)
            if hasattr(self.fluid, 'T'):
                self.fluid.solve_equations(self.dt)
                self.fluid.update_properties()
                self.fluid.update_boundary_nodes(self.dt)
            
            print(self.fluid._sources)
            sys.exit()
            self.phase_coupling(self.dt)

if __name__ == '__main__':
    ot = OpenTerrace(t_end=1800, dt=0.1, n_bed=5, n_fluid=20)

    ot.fluid.select_substance(substance='water')
    ot.fluid.select_domain(domain='1d_cylinder', D=1, H=5)
    ot.fluid.select_schemes(conv='upwind_1d', diff='central_difference_1d')
    ot.fluid.initialise(T=273.15, mdot=1)
    ot.fluid.define_bc(bc_type='dirichlet', parameter='T', position=np.s_[:,0], value=323.15)
    ot.fluid.define_bc(bc_type='neumann', parameter='T', position=np.s_[:,-1])
    ot.fluid.define_source_term(source_type='forced_convection_couple', h_type='constant', h_coeff=1200, slice=np.s_[0])
    ot.fluid.define_source_term(source_type='thermal_resistance', R=0.001, Tinf=273.15+20, slice=np.s_[0])

    ot.bed.select_substance(substance='magnetite')
    ot.bed.select_domain(domain='1d_sphere', D=0.05)
    ot.bed.select_schemes(diff='central_difference_1d')
    ot.bed.initialise(T=273.15)
    ot.bed.define_bc(bc_type='neumann', parameter='T', position=np.s_[:,-1])
    ot.bed.define_bc(bc_type='neumann', parameter='T', position=np.s_[:,0])
    ot.bed.define_source_term(source_type='forced_convection_couple', h_type='constant', h_coeff=1200, slice=np.s_[:,-1])
    
    ot.run_simulation()

    plt.plot(ot.fluid.domain.node_pos/(ot.fluid.domain.node_pos[-1]-ot.fluid.domain.node_pos[0]), ot.fluid.T[0,:], '-sb')
    plt.grid()
    plt.show()