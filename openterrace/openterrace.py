# Import OpenTerrace modules
import fluid_substances
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
    def __init__(self, t_end=3600, dt=1, n_fluid=1, n_bed=10):
        """Initialise OpenTerrace with control parameters"""
        self.t = 0
        self.t_end = t_end
        self.dt = dt
        self.fluid = self.Phase(n=n_fluid, _type='fluid', options='fluid_substances')
        self.bed = self.Phase(n=n_bed, n2=n_fluid, _type='bed', options='bed_substances')

    class Phase:
        def __init__(self, n=None, n2=1, _type=None, options=None):
            self.n = n
            self.n2 = n2
            self.options = options
            self._type = _type
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
            self.domain.node_pos = self.domain.node_pos(kwargs)
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

            if self.diff:
                self.D = np.zeros(((2,)+(self.T.shape)))
            if self.conv:
                self.F = np.zeros(((2,)+(self.T.shape)))

        def update_properties(self):
            """Updates properties based on specific enthalpy"""
            self.T = self.fcns.T(self.h)
            self.rho = self.fcns.rho(self.h)
            self.cp = self.fcns.cp(self.h)
            self.k = self.fcns.k(self.h)

            if self.diff:
                self.D = np.zeros(((2,)+(self.T.shape)))
                self.D[0,:,:] = self.k*self.domain.A[0]/self.domain.dx
                self.D[1,:,:] = self.k*self.domain.A[1]/self.domain.dx

            if self.conv:
                self.F = np.zeros(((2,)+(self.T.shape)))
                self.F[0,:,:] = self.mdot*self.cp
                self.F[1,:,:] = self.mdot*self.cp

        def define_bc(self, bc_type=None, parameter=None, position=None, value=None):
            """Specify boundary condition type"""
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
                    self.h[:,bc['position']] = self.fcns.h(bc['value'])
                if bc['type'] == 'neumann': 
                    if bc['position'] == [0]:
                        self.h[:,0] = self.h[:,1]
                    if bc['position'] == [1]:
                        self.h[:,-1] = self.h[:,-2]

        def update_boundary_nodes(self):
            """Update the nodes at the domain boundary"""
            pass

        def solve_equations(self, dt):
            if self.diff:
                self.h = self.h + self.diff(self.T, self.D)/(self.rho*self.domain.V)*dt
            if self.conv:
                self.h = self.h + self.conv(self.T, self.F)/(self.rho*self.domain.V)*dt
                
    def add_source_term(self, source_term=None, h=None, value=None):
        """Specify coupling type between the two phases"""

    def run_simulation(self):
        """This is the function full of magic."""
        for i in tqdm.tqdm(np.arange(0, self.t_end, self.dt)):
            self.bed.update_boundary_nodes()
            self.bed.solve_equations(self.dt)
            self.bed.update_properties()

    def phase_coupling(self):
        pass

if __name__ == '__main__':
    ot = OpenTerrace(t_end=600, dt=0.01, n_bed=100)

    # ot.fluid.select_substance(substance='water')
    # ot.fluid.select_domain(domain='1d_cylinder', D=1, H=5)
    # ot.fluid.select_scheme(conv='upwind_1d', diff='central_difference_1d')
    # ot.fluid.initialise(T=20+273.15, mdot=1)
    # ot.fluid.define_bc(bc_type='dirichlet', parameter='T', position=[0], value=80+273.15)
    # ot.fluid.define_bc(bc_type='neumann', parameter='T', position=[-1])
    # ot.fluid.enforce_bcs()

    ot.bed.select_substance(substance='magnetite')
    ot.bed.select_domain(domain='1d_sphere_2', D=0.05)
    ot.bed.select_scheme(diff='central_difference_1d')
    ot.bed.initialise(T=0)
    ot.bed.define_bc(bc_type='dirichlet', parameter='T', position=[0], value=100)
    ot.bed.define_bc(bc_type='neumann', parameter='T', position=[-1])
    ot.bed.enforce_bcs()
    
    ot.phase_coupling(source_term='forced_convection', h='constant', value=1200, position=[-1])
    ot.run_simulation()

    plt.plot(ot.bed.domain.node_pos, ot.bed.T[0,:],'-sk')
    plt.grid()
    plt.show()