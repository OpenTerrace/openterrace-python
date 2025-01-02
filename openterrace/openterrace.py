# Import OpenTerrace modules
from . import fluid_substances
from . import bed_substances
from . import domains
from . import diffusion_schemes
from . import convection_schemes
from . import boundary_conditions

# Import common Python modules
import sys
import tqdm
import numpy as np
import matplotlib
import time
matplotlib.use('agg')

class Setup:
    """OpenTerrace class."""

    def __init__(self, t_simulate:float=None, dt:float=None, t_start:float=0):
        """Initialise with various control parameters.

        Args:
            t_simulate (float): Start time in s
            dt (float): Time step size in s
        """
        self.t_simulate = t_simulate
        self.dt = dt
        self.coupling = []
        self.flag_coupling = False
        self.t = t_start
        
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
        """This is the function that couples the fluid and bed phase."""
        for couple in self.coupling:
            n_bed = self.Phase.instances[couple['fluid_phase']].domain.V/self.Phase.instances[couple['fluid_phase']].phi*(1-self.Phase.instances[couple['fluid_phase']].phi)/self.Phase.instances[couple['bed_phase']].domain.V0 #ok

            Q = couple['h_value']*self.Phase.instances[couple['bed_phase']].domain.A[-1][-1]*(self.Phase.instances[couple['fluid_phase']].T[0]-self.Phase.instances[couple['bed_phase']].T[:,-1])*self.dt #ok

            self.Phase.instances[couple['bed_phase']].h[:,-1] = self.Phase.instances[couple['bed_phase']].h[:,-1] + Q/(self.Phase.instances[couple['bed_phase']].rho[:,-1] * self.Phase.instances[couple['bed_phase']].domain.V[-1]) #ok

            self.Phase.instances[couple['fluid_phase']].h[0] = self.Phase.instances[couple['fluid_phase']].h[0] - n_bed * Q/(self.Phase.instances[couple['fluid_phase']].rho*self.Phase.instances[couple['fluid_phase']].domain.V) #ok
            
    def run_simulation(self, phases:list[str]=None):
        """If you want to run the simulation, you need to call this function. If data output is specified using the select_output function, the data will live in that specific phase instance. For more details on how to access the data, please refer to the tutorials."""
        
        t_start = self.t

        print("Simulation started at t = "+str(t_start)+" s")
        print("Simulation will run until t = "+str(t_start+self.t_simulate)+" s")
        print("Time step size is "+str(self.dt)+" s")
        pbar = tqdm.tqdm(desc="Simulating",total=(t_start+self.t_simulate)/self.dt)

        while self.t < t_start+self.t_simulate:
            for phase in phases:
                phase._save_data(self.t)
                phase._update_massflow_rate(self.t)
                phase._update_properties()
                phase._solve_equations(self.dt)

                if self.flag_coupling:
                    self._coupling()

            self.t = self.t+self.dt
            pbar.update()
        pbar.close()

class Phase:
    instances = []
    """Main class to create a phase."""

    def __init__(self, type:str=None):
        """Initialise a phase with number of control points and type.

        Args:
            type (str): Type of phase
        """

        valid_types = ['fluid','bed']
        if type not in valid_types:
            raise Exception("Type \'"+type+"\' specified. Valid options for types are:", valid_types)

        self.bc = []
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

    def select_domain_type(self, domain:str=None):
        """Select domain shape and initialise constants.
            
        Args:
            domain (str): Domain type
        """

        if not domain:
            raise Exception("Keyword 'domain' not specified.")
        if not domain in globals()['domains'].__all__:
            raise Exception("domain \'"+domain+"\' specified. Valid options for domain are:", globals()['domains'].__all__)
        self.domain = getattr(globals()['domains'], domain).Domain()

    def create_domain(self, **kwargs):
        """Selects domain size and parameters.

        Args:
            **kwargs (float): Dimensions of domain to be specified depending on the domain type
        """

        for var in self.domain.required_input():
            if not var in kwargs:
                raise Exception("Keyword \'"+var+"\' is missing for domain \'"+self.domain.__module__+"\'")

        self.domain.__dict__.update(kwargs)
        self.domain.update_parameters()

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

    def select_initial_temperature(self, T:float=None):
        """Initialises temperature field.

        Args:
            T (float): List of length n with initial temperatures
        """
        
        self.T = np.tile(T,self.domain.n)
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

    def select_bc(self, position:int=None, bc_type:str=None, value:float=None):
        """Specify boundary condition type.
                    
        Args:
            position (int): 0 or -1
            bc_type (str): Type of boundary condition            
            value (float): Value of boundary condition
        """

        if bc_type is None:
            raise Exception("Keyword 'bc_type' not specified.")
        if not bc_type in globals()['boundary_conditions'].__all__:
            raise Exception("bc_type \'"+bc_type+"\' specified. Valid options for bc_type are:", globals()['boundary_conditions'].__all__)

        if not position in [0,-1]:
            raise Exception("Keyword 'position' should be either 0 or -1.")
        if value is None:
            raise Exception("Keyword 'value' not specified.")
      
        for bc_cond in self.bc:
            if bc_cond['position'] == np.s_[:,position]:
                bc_cond['type'] = bc_type
                bc_cond['value'] = value
                break
        else:
            self.bc.append({'type': bc_type, 'value': value, 'position': np.s_[:,position]})

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
        if not hasattr(self, 'mdot_array'):
            raise Exception("Mass flow rate not specified.")

        if self.mdot_array.ndim == 0:
            self.mdot = self.mdot_array

        if self.mdot_array.ndim == 2:
            self.mdot = np.interp(t, self.mdot_array[:,0], self.mdot_array[:,1])
            
    def _update_properties(self):
        """Update properties at each time step."""
            
        self.T = self.fcns.T(self.h)
        self.rho = self.fcns.rho(self.h)
        self.cp = self.fcns.cp(self.h)

        if hasattr(self, 'diff'):
            self.k = self.fcns.k(self.h)
            self.D[0] = self.k*self.domain.A[0]/self.domain.dx
            self.D[1] = self.k*self.domain.A[1]/self.domain.dx
            
        if hasattr(self, 'conv'):
            self.F[0] = self.mdot*self.cp
            self.F[1] = self.mdot*self.cp

    def _update_boundary_nodes(self, dt:float=None):
        """Update boundary nodes.
            
        Args:
            dt (float): Time step size
        """

        for bc in self.bc:
            if bc['type'] == 'fixed_value':
                self.h[bc['position']] = self.fcns.h(bc['value'])
            if bc['type'] == 'zero_gradient':
                if bc['position'] == np.s_[:,0]:
                    self.h[bc['position']] = self.h[bc['position']] + (2*self.T[:,1]*self.D[1,:,0] - 2*self.T[:,0]*self.D[1,:,0] - self.F[0,:,1]*self.T[:,1] + self.F[1,:,0]*self.T[:,0]) / (self.rho[:,0]*self.domain.V[0])*dt
                if bc['position'] == np.s_[:,-1]:
                    self.h[bc['position']] = self.h[bc['position']] + (2*self.T[:,-2]*self.D[0,:,-1] - 2*self.T[:,-1]*self.D[0,:,-1] + self.F[1,:,-2]*self.T[:,-2] - self.F[0,:,-1]*self.T[:,-1]) / (self.rho[:,-1]*self.domain.V[-1])*dt

    def _update_source(self, dt:float=None):
        """Update source term.
            
        Args:
            dt (float): Time step size
        """

        for source in self.sources:
            self.h = self.h + (source['T_inf']-self.T)*2 / source['R'] * dt/(self.rho*self.domain.V)

    def _solve_equations(self, dt:float=None):

        """Solve equations at each time step.

        Args:
            t (float): Current time
            dt (float): Time step size
        """

        self._update_boundary_nodes(dt)
        if hasattr(self, 'diff'):
            self.h = self.h + self.diff(self.T, self.D)/(self.rho*self.domain.V)*dt
        if hasattr(self, 'conv'):
            self.h = self.h + self.conv(self.T, self.F)/(self.rho*self.domain.V)*dt
        if self.sources is not None:
            self._update_source(dt)