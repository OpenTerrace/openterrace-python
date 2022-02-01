import numpy as np
import pathlib
import yaml
import shutil

import fluids
import solids
import shapes

class Parameters():
    def read_input_data(self, inputfile=None, simulation_folder='simulations'):
        """Read a Open Terrace input file in .yaml format
        """
        self.cwd = pathlib.Path(__file__).resolve().parent
        self.inputfile_path = self.cwd / pathlib.Path(inputfile)
        try: 
            with open(self.inputfile_path) as f:
                self.__dict__.update(yaml.load(f, Loader=yaml.loader.SafeLoader))
                self.case_path = self.cwd / simulation_folder / self.inputfile_path.stem
        except:
            raise Exception("Inputfile not found at ", pathlib.Path(inputfile).absolute())
    
    def initialise_case(self, overwrite=False):
        """Initialises the case folder to store simulation data
        """
        if self.case_path.absolute().exists():
            if overwrite is True:
                shutil.rmtree(self.case_path.absolute())
                print("Deleted already existing case folder")
            else:
                raise Exception('Case folder already exists and overwrite is False')
        self.case_path.absolute().mkdir(parents=True, exist_ok=False)
        print("New case folder created")
        self.t = 0
        print("Initialised with time t=0 s")

    def update_massflow_rate(self, t):
        return np.interp(t, [row[0] for row in self.massflow_vs_time], [row[1] for row in self.massflow_vs_time])
    
    def update_inlet_temperature(self, t):
        return np.interp(t, [row[0] for row in self.inlettemp_vs_time], [row[1] for row in self.inlettemp_vs_time])

class Fluid():
    def __init__(self, params):
        try:
            self.fcns = getattr(fluids, params.fluid)
        except:
            raise Exception("Valid options for fluid are:",fluids.__all__) 
        self.T = np.full((params.ny_tank+2,1), params.update_inlet_temperature(0))
        self.Told = np.copy(self.T)

    def update_props(self, **kwargs):
        if kwargs['method'] == 'constprops':
            try:
                self.rho = self.fcns.rho(np.full_like(self.T, kwargs['T']))
                self.cp = self.fcns.cp(np.full_like(self.T, kwargs['T']))
                self.k = self.fcns.k(np.full_like(self.T, kwargs['T']))
            except:
                raise Exception("'T' not specfied")
        elif kwargs['method'] == 'varprops':
            self.rho = self.fcns.rho(self.T)
            self.cp = self.fcns.cp(self.T)
            self.k = self.fcns.k(self.T)  
        else:
            raise Exception(kwargs['method']+" is not a valid method.")
            
        self.alpha = self.k/(self.rho*self.cp)

class Particle():
    def __init__(self, params):
        try:
            self.fcns = getattr(solids, params.solid)
        except:
            raise Exception("Valid options for solid are:",solids.__all__)

        try:
            self.shape = getattr(shapes, params.shape)
        except:
            raise Exception("Valid options for shape are:",shapes.__all__)

        self.T = np.empty(params.nx_particle)
        self.Told = np.empty(params.nx_particle)

    def update_props(self, **kwargs):
        if kwargs['method'] == 'constprops':
            try:
                self.rho = self.fcns.rho(np.full_like(self.T, kwargs['T']))
                self.cp = self.fcns.cp(np.full_like(self.T, kwargs['T']))
                self.k = self.fcns.k(np.full_like(self.T, kwargs['T']))
            except:
                raise Exception("'T' not specfied")
        elif kwargs['method'] == 'varprops':
            self.rho = self.fcns.rho(self.T)
            self.cp = self.fcns.cp(self.T)
            self.k = self.fcns.k(self.T)  
        else:
            raise Exception(kwargs['method']+" is not a valid method.")
            
        self.alpha = self.k/(self.rho*self.cp)




        self.rho = self.fcns.rho(self.T)
        self.k = self.fcns.k(self.T)
        self.cp = self.fcns.cp(self.T)