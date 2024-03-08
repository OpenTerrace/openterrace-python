# Import OpenTerrace modules
from . import fluid_substances
from . import bed_substances
from . import domains
from . import diffusion_schemes
from . import convection_schemes

# Import common Python modules
import sys
import tqdm
import numpy as np
import matplotlib
matplotlib.use('agg')

class Simulate:
    """OpenTerrace class."""

    def __init__(self, t_start:float=0, t_end:float=None, dt:float=None):
        """Initialise with various control parameters.

        Args:
            t_start (float): Start time in s
            t_end (float): End time in s
            dt (float): Time step size in s
        """
        self.t_start = t_start
        self.t_end = t_end
        self.dt = dt
        self.coupling = []
        self.flag_coupling = False

    def create_phase(self, n:int=None, n_other:int=1, type:str=None):
        """Creates a fluid or bed phase.

        Args:
            n (int): Number of discretisations
            n_other (int): Number of discretisations of interacting phase. If you are defining a bed phase within a tank. Then n_other is the number of discretisations of the fluid phase.
            type (str): Phase type
        """

        valid_types = ['fluid','bed']
        if type not in valid_types:
            raise Exception("Type \'"+type+"\' specified. Valid options for types are:", valid_types)
        return self.Phase(self, n, n_other, type)
        
    def select_coupling(self, fluid_phase:int=None, bed_phase:int=None, h_exp:str=None, h_value:float=None):
        """Selects coupling of a fluid and bed phase

        Args:
            fluid_phase (int): phase number
            bed_phase (int): phase number
            h_exp (str): Predefined function for convective heat transfer
            h_value (float): Convective heat transfer coefficient in W/(m^2 K)
        """

        valid_h_exp = ['constant']
        if h_exp not in valid_h_exp:
            raise Exception("h_exp \'"+h_exp+"\' specified. Valid options for h_exp are:", valid_h_exp)
        
        self.coupling.append({"fluid_phase":fluid_phase, "bed_phase":bed_phase, "h_exp":h_exp, "h_value":h_value})
        self.flag_coupling = True

    def _coupling(self):
        for couple in self.coupling:
            Q = couple['h_value']*self.Phase.instances[couple['bed_phase']].domain.A[-1][-1]*(self.Phase.instances[couple['fluid_phase']].T[0]-self.Phase.instances[couple['bed_phase']].T[:,-1])*self.dt
            self.Phase.instances[couple['bed_phase']].h[:,-1] = self.Phase.instances[couple['bed_phase']].h[:,-1] + Q/(self.Phase.instances[couple['bed_phase']].rho[:,-1] * self.Phase.instances[couple['bed_phase']].domain.V[-1])
            self.Phase.instances[couple['fluid_phase']].h[0] = self.Phase.instances[couple['fluid_phase']].h[0] - (1-self.Phase.instances[couple['fluid_phase']].phi)/self.Phase.instances[couple['fluid_phase']].phi * self.Phase.instances[couple['fluid_phase']].domain.V/self.Phase.instances[couple['bed_phase']].domain.V0 * Q/(self.Phase.instances[couple['fluid_phase']].rho*self.Phase.instances[couple['fluid_phase']].domain.V)

    def run_simulation(self):
        """This is the function full of magic."""

        for t in tqdm.tqdm(np.arange(self.t_start, self.t_end+self.dt, self.dt)):
            for phase_instance in self.Phase.instances:
                phase_instance._save_data(t)
                phase_instance._solve_equations(t, self.dt)
                phase_instance._update_properties()
            if self.flag_coupling:
                self._coupling()
    class Phase:
        instances = []
        """Main class to define either the fluid or bed phase."""

        def __init__(self, outer=None, n:int=None, n_other:int=None, type:str=None):
            """Initialise a phase with number of control points and type.

            Args:
                n_self (int): Number of discretisations for the given phase
                n_other (int): Number of discretisations for the other phase
                type (str): Type of phase
            """

            self.outer = outer
            self.__class__.instances.append(self)
            self.n = n
            self.n_other = n_other
            
            self.phi = 1
            self.bcs = []
            self.sources = []

            self._flag_save_data = False
            self.type = type

        def select_substance_on_the_fly(self, cp:float=None, rho:float=None, k:float=None):
            """Defines and selects a new substance on-the-fly. This is useful for defining a substance for testing purposes with temperature independent properties.

            Args:
                cp (float): Specific heat capacity in J/(kg K)
                rho (float): Density in kg/m^3
                k (float): Thermal conductivity in W/(m K)
            """
            class dummy:
                pass
            self.fcns = dummy()
            self.fcns.h = lambda T: np.ones_like(T)*T*cp
            self.fcns.T = lambda h: np.ones_like(h)*h/cp
            self.fcns.cp = lambda h: np.ones_like(h)*cp
            self.fcns.k = lambda h: np.ones_like(h)*k
            self.fcns.rho = lambda h: np.ones_like(h)*rho

        def select_substance(self, substance:str=None):
            """Selects one of the predefined substancers.

            Args:
                substance (str): Substance name
            """

            valid_substances = globals()[self.type+'_substances'].__all__
            if not substance:
                raise Exception("Keyword 'substance' not specified.")
            if not substance in valid_substances:
                raise Exception(substance+" specified as "+self.type+" substance. Valid "+self.type+" substances are:", valid_substances)
            self.fcns = getattr(globals()[self.type+'_substances'], substance)

        def select_h_coeff(self, h_exp:str=None, value:float=None):
            """Selects an expression for the heat transfer coefficient.

            Args:
                h_exp (str): Heat transfer coefficient expression
                value (float): Heat transfer coefficient value
            """

            valid_correlations = ['constant']
            if correlation not in valid_correlations:
                raise Exception("correlation \'"+correlation+"\' specified. Valid options for correlation are:", valid_correlations)
            self.fcns.h_correlation = getattr(globals()['heat_transfer_correlations'], correlation)

        def select_domain_shape(self, domain:str=None, **kwargs):
            """Select domain shape and initialise constants.
            
            Args:
                domain (str): Domain type
                additional arguments (float): Dimensions of domain
            """

            if not domain:
                raise Exception("Keyword 'domain' not specified.")
            if not domain in globals()['domains'].__all__:
                raise Exception("domain \'"+domain+"\' specified. Valid options for domain are:", self.valid_domains)

            kwargs['n'] = self.n
            self.domain = getattr(globals()['domains'], domain)
            self.domain.type = domain
            self.domain.validate_input(kwargs, domain)
            self.domain.shape = self.domain.shape(kwargs)
            self.domain.dx = self.domain.dx(kwargs)
            self.domain.A = self.domain.A(kwargs)
            self.domain.V = self.domain.V(kwargs)
            self.domain.V0 = self.domain.V0(kwargs)
            self.node_pos = self.domain.node_pos(kwargs)

        def select_porosity(self, phi:float=1):
            """Select porosity from 0 to 1, e.g. filling the domain with the phase up to a certain degree.
            
            Args:
                phi (float): Porosity value
            """

            self.domain.V = self.domain.V*phi
            self.phi = phi

        def select_schemes(self, diff:str=None, conv:str=None):
            """Imports the specified diffusion and convection schemes.

            Args:
                diff (str): Differenctial scheme
                conv (str): Convection scheme
            """

            if self.domain.type == 'lumped':
                raise Exception("'lumped' has been selected as domain type. Please don't specify a discretisation scheme.")

            if diff is not None:
                try:
                    self.diff = getattr(getattr(globals()['diffusion_schemes'], diff), diff)
                except:
                    raise Exception("Diffusion scheme \'"+diff+"\' specified. Valid options for diffusion schemes are:", diffusion_schemes.__all__)

            if conv is not None:
                try:
                    self.conv = getattr(getattr(globals()['convection_schemes'], conv), conv)
                except:
                    raise Exception("Convection scheme \'"+conv+"\' specified. Valid options for convection schemes are:", convection_schemes.__all__)

        def select_initial_conditions(self, T:list[float]=None):
            """Initialises temperature field.

            Args:
                T (float): List of length n with initial temperatures
            """
            
            if np.array(T).size == 1:
                self.T = np.tile(T,(np.append(self.n_other,self.domain.shape)))   
            elif np.array(T).size == self.n:
                self.T = np.tile(T,(np.append(self.n_other,1)))
            else: Exception("Length of T must be 1 or equal to n")

            self.h = self.fcns.h(self.T)
            self.T = self.fcns.T(self.h)
            self.rho = self.fcns.rho(self.h)
            self.cp = self.fcns.cp(self.h)
            self.k = self.fcns.k(self.h)
            self.D = np.zeros(((2,)+(self.T.shape)))
            self.F = np.zeros(((2,)+(self.T.shape)))
            self.S = np.zeros(self.T.shape)

        def select_massflow(self, mdot:list[float]=None):
            """Initialises mass flow rate field.

            Args:
                mdot (float): Array of mass flow rate. Column 0 is time and column 1 is mass flow rate
            """

            self.mdot_array = np.array(mdot)

        def select_bc(self, bc_type:str=None, parameter:str=None, position=None, value:float=None):
            """Specify boundary condition type.
                    
            Args:
                bc_type (str): Type of boundary condition
                parameter (str): Which field it applies to
                position (int): indices of which cells it applies to
                value (float): Value of boundary condition
            """

            valid_bc_types = ['fixed_value','zero_gradient']
            if bc_type not in valid_bc_types:
                raise Exception("bc_type \'"+bc_type+"\' specified. Valid options for bc_type are:", valid_bc_types)
            valid_parameters = ['T','mdot']
            if parameter not in valid_parameters:
                raise Exception("parameter \'"+parameter+"\' specified. Valid options for parameter are:", valid_parameters)
            if not position:
                raise Exception("Keyword 'position' not specified.")
            if value is None and bc_type=='fixed_value':
                raise Exception("Keyword 'value' is needed for fixed_value type bc.")
            self.bcs.append({'type': bc_type, 'parameter': parameter, 'position': position, 'value': np.array(value)})

        def add_sourceterm_thermal_resistance(self, R:list[float], T_inf:list[float]):
            """Specify a thermal resistance source term.
                    
            Args:
                R (float): List of thermal resistances
                T_inf (float): List of fluid temperatures
            """
            if not len([R]) in [1,self.n]:
                raise Exception("Length of R must be 1 or equal to n")

            if not len([T_inf]) in [1,self.n]:
                raise Exception("Length of T_inf must be 1 or equal to n")

            self.sources.append({'R': R, 'T_inf': T_inf})

        def select_output(self, times:list[float]=None, output_parameters:list[str]=['T']):
            """Specify output times.

            Args:
                times (float): List of times to output data
            """

            self.output_parameters = output_parameters
            class Data(object):
                pass
            self.data = Data()
            self.data.time = np.intersect1d(np.array(times), np.arange(self.outer.t_start, self.outer.t_end+self.outer.dt, self.outer.dt))
            for parameter in output_parameters:
                setattr(self.data,parameter, np.full((len(self.data.time), self.n_other, self.n),np.nan))
                self._flag_save_data = True
                self._q = 0

        def _save_data(self, t:float=None):
            """Save data at specified times.
            
            Args:
                t (float): Current time
            """

            if self._flag_save_data:
                if t in self.data.time:
                    for parameter in self.output_parameters:
                        getattr(self.data,parameter)[self._q] = getattr(self,parameter)
                    self._q = self._q+1

        def _update_massflow_rate(self, t:float):
            """Update mass flow rate at specified times.
            
            Args:
                t (float): Current time
            """

            if self.mdot_array.ndim == 0:
                self.mdot = np.tile(self.mdot_array,(np.append(self.n_other,self.domain.shape)))
            elif self.mdot_array.ndim == 2:
                self.mdot = np.interp(t, self.mdot_array[:,0], self.mdot_array[:,1])

        def _update_properties(self):
            """Update properties at each time step."""
            
            self.T = self.fcns.T(self.h)
            self.rho = self.fcns.rho(self.h)
            self.cp = self.fcns.cp(self.h)

            if hasattr(self, 'diff'):
                self.k = self.fcns.k(self.h)
                self.D[0,:,:] = self.k*self.domain.A[0]/self.domain.dx
                self.D[1,:,:] = self.k*self.domain.A[1]/self.domain.dx

            if hasattr(self, 'conv'):
                self.F[0,:,:] = self.mdot*self.cp
                self.F[1,:,:] = self.mdot*self.cp

        def _update_boundary_nodes(self, t:float=None, dt:float=None):
            """Update boundary nodes.
            
            Args:
                t (float): Current time
                dt (float): Time step size
            """

            for bc in self.bcs:
                if bc['type'] == 'fixed_value':
                    self.h[bc['position']] = self.fcns.h(bc['value'])
                if bc['type'] == 'fixed_value_timevarying':
                    self.h[bc['position']] = self.fcns.h(np.interp(t,bc['value'][:,0],bc['value'][:,1]))
                if bc['type'] == 'zero_gradient':
                    if bc['position'] == np.s_[:,0]:
                        self.h[bc['position']] = self.h[bc['position']] + (self.T[:,1]*self.D[1,:,0] - self.T[:,0]*self.D[1,:,0] - self.F[0,:,1]*self.T[:,1] + self.F[1,:,0]*self.T[:,0]) / (self.rho[:,0]*self.domain.V[0])*dt
                    if bc['position'] == np.s_[:,-1]:
                        self.h[bc['position']] = self.h[bc['position']] + (self.T[:,-2]*self.D[0,:,-1] - self.T[:,-1]*self.D[0,:,-1] + self.F[1,:,-2]*self.T[:,-2] - self.F[0,:,-1]*self.T[:,-1]) / (self.rho[:,-1]*self.domain.V[-1])*dt

        def _update_source(self, dt:float=None):
            """Update source term.
            
            Args:
                dt (float): Time step size
            """

            for source in self.sources:
                self.h = self.h + (source['T_inf']-self.T) / source['R'] * dt/(self.rho*self.domain.V)

        def _solve_equations(self, t:float=None, dt:float=None):
            """Solve equations at each time step.

            Args:
                t (float): Current time
                dt (float): Time step size
            """

            self._update_boundary_nodes(t, dt)
            if hasattr(self, 'diff'):
                self.h = self.h + self.diff(self.T, self.D)/(self.rho*self.domain.V)*dt
            if hasattr(self, 'conv'):
                self._update_massflow_rate(t)
                self.h = self.h + self.conv(self.T, self.F)/(self.rho*self.domain.V)*dt
            if self.sources is not None:
                self._update_source(dt)