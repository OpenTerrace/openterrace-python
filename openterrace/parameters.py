import numpy as np
import pathlib
import yaml
from yaml.loader import SafeLoader
import fluids
import solids
import shapes

class Parameters():
    def read_input_data(self, inputfile):
        try: 
            with open(pathlib.Path(inputfile).absolute()) as f:
                self.input_data = yaml.load(f, Loader=SafeLoader)

                #self.test = getattr(fluids, params.input_data['fluid'])
                # self.t_end = self.input_data['t_end']
                # self.dt = self.input_data['dt']
                # self.h_tank = self.input_data['h_tank']
                # self.d_tank = self.input_data['d_tank']
                # self.ny_tank = self.input_data['ny_tank']

        except:
            raise Exception("Inputfile not found at ", pathlib.Path(inputfile).absolute())
    
    def update_massflow_rate(self, t):
        self.mdot = np.interp(t, [row[0] for row in self.input_data['massflow_vs_time']], [row[1] for row in self.input_data['massflow_vs_time']])
    
    def update_inlet_temperature(self, t):
        self.Tin = np.interp(t, [row[0] for row in self.input_data['inlettemp_vs_time']], [row[1] for row in self.input_data['inlettemp_vs_time']])

class Fluid():
    def __init__(self, params):
        try:
            self.fcns = getattr(fluids, params.input_data['fluid'])
        except:
            raise Exception("Valid options for fluid are:",fluids.__all__) 
        self.rho = 2

class Particle():
    def __init__(self, params):
        try:
            self.fcns = getattr(solids, params.input_data['solid'])
        except:
            raise Exception("Valid options for solid are:",solids.__all__)

        try:
            self.shape = getattr(shapes, params.input_data['shape'])
        except:
            raise Exception("Valid options for shape are:",shapes.__all__)

            # self.T = np.full((const.nx_particles, const.nx_tank), const.Tinit)
            # self.T_old = np.copy(self.T)
            # self.rho = prop.solid.rho(self.T)
            # self.k = prop.solid.k(self.T)
            # self.cp = prop.solid.cp(self.T)
            # self.bc = const.bc
            # self.h = np.full(const.nx_tank, 200)
