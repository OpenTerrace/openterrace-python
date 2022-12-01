# # Import OpenTerrace modules
from . import fluid_substances
from . import bed_substances
from . import domains
from . import diffusion_schemes
from . import convection_schemes

# Import common Python modules
import __main__
import tqdm
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.animation as anim

class Simulate:
    """OpenTerrace class."""
    def __init__(self, t_end:float=None, dt:float=None, n_fluid:float=1, n_bed:float=2):
        """Initialise with various control parameters.

        Args:
            t_end (float): End time in s
            dt (float): Time step size in s
            n_fluid (float): Number of discretisations for fluid phase
            n_bed (float): Number of discretisations for bed phase
        """
        self.t_start = 0
        self.t_end = t_end
        self.dt = dt
        self.fluid = self.Phase(n=n_fluid, n2=1, _type='fluid')
        self.bed = self.Phase(n=n_bed, n2=n_fluid, _type='bed')
        self.sources = []
        self.coupling = False
        self.saved_data = []
        self.list_postprocess = []
        self.save_data_flag = np.full(int(np.floor(t_end/dt))+1, False)
        self.output_animation_flag = False
        self.filename = __main__.__file__.split('/')[-1].rsplit( ".", 1)[0]

    class Phase:
        """Main class to define either the fluid or bed phase."""
        def __init__(self, n:int=None, n2:int=None, _type:str=None):
            self.n = n
            self.n2 = n2
            self._type = _type
            self.bcs = []
            self.sources = []
            self.phi = 1
            self._valid_inputs(_type)

        def _valid_inputs(self, _type:str):
            self.valid_domains = globals()['domains'].__all__
            self.valid_substances = globals()[self._type+'_substances'].__all__

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
            if not substance:
                raise Exception("Keyword 'substance' not specified.")
            if not substance in self.valid_substances:
                raise Exception(substance+" specified as "+self._type+" substance. Valid "+self._type+" substances are:", self.valid_substances)
            self.fcns = getattr(globals()[self._type+'_substances'], substance)

        def select_domain_shape(self, domain:str=None, **kwargs):
            """Select domain shape and initialise constants."""
            kwargs['n'] = self.n
            if not domain:
                raise Exception("Keyword 'domain' not specified.")
            if not domain in globals()['domains'].__all__:
                raise Exception("domain \'"+domain+"\' specified. Valid options for domain are:", self.valid_domains)
            self.domain = getattr(globals()['domains'], domain)
            self.domain.validate_input(kwargs, domain)
            self.domain.shape = self.domain.shape(kwargs)
            self.domain.node_pos = self.domain.node_pos(kwargs)
            self.domain.dx = self.domain.dx(kwargs)
            self.domain.A = self.domain.A(kwargs)
            self.domain.V = self.domain.V(kwargs)

        def select_porosity(self, phi:float=1):
            self.domain.V = self.domain.V*phi
            self.phi = phi

        def select_schemes(self, diff:str=None, conv:str=None):
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

        def select_initial_conditions(self, T:float=None, mdot:float=None):
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

        def select_bc(self, bc_type=None, parameter=None, position=None, value=None):
            """Specify boundary condition type"""
            valid_bc_types = ['neumann','dirichlet','timevarying_dirichlet']
            if bc_type not in valid_bc_types:
                raise Exception("bc_type \'"+bc_type+"\' specified. Valid options for bc_type are:", valid_bc_types)
            valid_parameters = ['T','mdot']
            if parameter not in valid_parameters:
                raise Exception("parameter \'"+parameter+"\' specified. Valid options for parameter are:", valid_parameters)
            if not position:
                raise Exception("Keyword 'position' not specified.")
            if value is None and bc_type=='dirichlet':
                raise Exception("Keyword 'value' is needed for dirichlet type bc.")
            self.bcs.append({'type': bc_type, 'parameter': parameter, 'position': position, 'value': value})

        def select_source_term(self, **kwargs):
            valid_source_types = ['thermal_resistance']
            if kwargs['source_type'] not in valid_source_types:
                raise Exception("source_type \'"+kwargs['source_type']+"\' specified. Valid options for source_type are:", valid_source_types)
            if kwargs['source_type'] == 'thermal_resistance':
                required = ['R','T_inf', 'position']
                for var in required:
                    if not var in kwargs:
                        raise Exception("Keyword \'"+var+"\' not specified for source of type \'"+kwargs['source_type']+"\'")
            self.sources.append(kwargs)

        def _update_properties(self):
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

        def _update_boundary_nodes(self, dt):
            """Update boundary nodes"""
            for bc in self.bcs:
                if bc['type'] == 'dirichlet':
                    self.h[bc['position']] = self.fcns.h(bc['value'])
                if bc['type'] == 'neumann':
                    if bc['position'] == np.s_[:,0]:
                        self.h[bc['position']] = self.h[bc['position']] + (2*self.T[:,1]*self.D[1,:,0] - 2*self.T[:,0]*self.D[1,:,0] - self.F[0,:,1]*self.T[:,1] + self.F[1,:,0]*self.T[:,0]) / (self.rho[:,0]*self.domain.V[0])*dt
                    if bc['position'] == np.s_[:,-1]:
                        self.h[bc['position']] = self.h[bc['position']] + (2*self.T[:,-2]*self.D[0,:,-1] - 2*self.T[:,-1]*self.D[0,:,-1] + self.F[1,:,-2]*self.T[:,-2] - self.F[0,:,-1]*self.T[:,-1]) / (self.rho[:,-1]*self.domain.V[-1])*dt

        def _update_source(self, dt):
            for source in self.sources:
                if source['source_type'] == 'thermal_resistance':
                    self.h[source['position']] = self.h[source['position']] + (2/source['R'] * (source['T_inf']-self.T[source['position']])) / (self.rho[source['position']]*self.domain.V[source['position'][1]])*dt

        def _solve_equations(self, dt):
            if self.diff is not None:
                self.h = self.h + self.diff(self.T, self.D)/(self.rho*self.domain.V)*dt
            if self.conv is not None:
                self.h = self.h + self.conv(self.T, self.F)/(self.rho*self.domain.V)*dt
            if self.sources is not None:
                self._update_source(dt)

    def select_coupling(self, h_coeff='constant', h_value=None):
        self.coupling = True
        valid_h_coeff = ['constant']
        if h_coeff not in valid_h_coeff:
            raise Exception("h_coeff \'"+h_coeff+"\' specified. Valid options for h_coeff are:", valid_h_coeff)
        if h_coeff == 'constant':
            self.h_value = h_value

    def _couple(self):
        Q = self.h_value*self.bed.domain.A[1,-1]*(self.fluid.T[0]-self.bed.T[:,-1])*self.dt
        self.bed.h[:,-1] = self.bed.h[:,-1] + Q/(self.bed.rho[:,-1]*self.bed.domain.V[-1])
        self.fluid.h[0] = self.fluid.h[0] - (1-self.fluid.phi)*(self.fluid.domain.V/self.fluid.phi) / np.sum(self.bed.domain.V) * Q/(self.fluid.rho*self.fluid.domain.V)

    def output_data(self):
        pass

    def output_animation(self, save_int:int=None, animate_data_flag:bool=False):
        if not save_int:
            raise Exception("Keyword 'save_int' not specified.")
        self.save_int = save_int
        self.saved_bed_data = np.zeros((len(np.arange(self.t_start,self.t_end,save_int*self.dt)), self.fluid.n, self.bed.n))
        self.saved_fluid_data = np.zeros((len(np.arange(self.t_start,self.t_end,save_int*self.dt)), self.fluid.n))
        self.saved_time_data = np.zeros(len(np.arange(self.t_start,self.t_end,save_int*self.dt)))
        self.save_data_flag[range(0, int(np.floor(self.t_end/self.dt))+1, save_int)] = True
        self.output_animation_flag = True

    def _create_animation(self, phase=None, xdata=None, ydata=None):
        fig, ax = plt.subplots()
        fig.tight_layout(pad=2)
        ymin = np.min(ydata)-273.15
        ymax = np.max(ydata)-273.15
        xmin = np.min(xdata)
        xmax = np.max(xdata)

        def _update(frame):
            x = xdata
            y = ydata[frame]
            ax.clear()
            ax.set_xlim(xmin, xmax)
            ax.set_ylim(ymin, ymax)
            ax.set_xlabel('Position (m)')
            ax.set_ylabel('Temperature (C)')
            ax.grid()
            ax.plot(x, y.T-273.15, color = '#4cae4f')
            ax.text(.05, .95, 'Simulated with OpenTerrace', ha='left', va='top', transform=ax.transAxes, color = '#4cae4f',
                bbox=dict(facecolor='white',boxstyle="square,pad=0.5", alpha=0.5))
            ax.set_title('Time: ' + str(np.round(self.saved_time_data[frame], decimals=2)) + ' s')

        ani = anim.FuncAnimation(fig, _update, frames=np.arange(int(np.floor(self.t_end/(self.dt*self.save_int)))))
        ani.save(filename='animation_'+self.filename+'_'+phase+'.gif', writer=anim.PillowWriter(fps=10),progress_callback=lambda i, n: print(f'Saving frame {i} of {n}'))

    def run_simulation(self):
        """This is the function full of magic."""
        i = 0
        for t in tqdm.tqdm(np.arange(self.t_start, self.t_end, self.dt)):
            if hasattr(self.bed, 'T'):
                self.bed._update_boundary_nodes(self.dt)
                self.bed._solve_equations(self.dt)
                self.bed._update_properties()
            
            if hasattr(self.fluid, 'T'):
                self.fluid._update_boundary_nodes(self.dt)
                self.fluid._solve_equations(self.dt)
                self.fluid._update_properties()

            if self.coupling:
                self._couple()

            if self.save_data_flag[i]:
                if np.mod(i, self.save_int) == 0:
                    self.saved_time_data[int(i/self.save_int)] = t
                    if hasattr(self.bed, 'T'):
                        self.saved_bed_data[int(i/self.save_int),:,:] = self.bed.T
                    if hasattr(self.fluid, 'T'):
                        self.saved_fluid_data[int(i/self.save_int),:] = self.fluid.T
            i = i+1

        if self.output_animation_flag:
            if hasattr(self.bed, 'T'):
                self._create_animation(phase='bed', xdata=self.bed.domain.node_pos, ydata=self.saved_bed_data)
            if hasattr(self.fluid, 'T'):
                self._create_animation(phase='fluid', xdata=self.fluid.domain.node_pos, ydata=self.saved_fluid_data)