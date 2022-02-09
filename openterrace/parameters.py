import numpy as np
import pathlib
import yaml
import shutil

import fluids
import solids
import shapes

class Parameters():
    def read_input_data(self, inputfile=None, storagefolder=None):
        """Read a Open Terrace input file in .yaml format
        """
        self.cwd = pathlib.Path(__file__).resolve().parent
        self.inputfile_path = self.cwd / pathlib.Path(inputfile)
        try: 
            with open(self.inputfile_path) as f:
                self.__dict__.update(yaml.load(f, Loader=yaml.loader.SafeLoader))
                self.case_path = self.cwd / storagefolder / self.inputfile_path.stem
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
        self.t_array = np.linspace(0,self.t_end,int(self.t_end/(self.dt)+1))
        self.t = self.t_array[0]
        print("Initialised with time t = 0 s")

class Fluid():
    def __init__(self, params):
        try:
            self.fcns = getattr(fluids, params.fluid)
        except:
            raise Exception("Valid options for fluid are:",fluids.__all__)
        
        self.T = np.empty((params.ny_tank+2,1))
        self.Told = np.copy(self.T)
        self.mdot = np.empty(1)

    def initialise_temp(self, **kwargs):
        validlist = ['const']
        if not kwargs['method'] in validlist:
            raise Exception(kwargs['method']+" is not a valid option. Valid options are "+str(validlist))

        if kwargs['method'] == 'const':
            try:
                self.T[:] = kwargs['T']
                self.Told[:] = kwargs['T']
            except:
                raise Exception("'T' not specfied")

    def update_mdot(self, x, t):
        self.mdot = np.interp(t, [row[0] for row in x], [row[1] for row in x])

    def update_Tin(self, x, t):
        self.T[0] = np.interp(t, [row[0] for row in x], [row[1] for row in x])

    def update_props(self):
        self.rho = self.fcns.rho(self.T)
        self.cp = self.fcns.cp(self.T)
        self.k = self.fcns.k(self.T)   
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

        self.T = np.empty((params.nx_particle, params.ny_tank))
        self.Told = np.copy(self.T)

    def initialise_temp(self, **kwargs):
        validlist = ['const']
        if not kwargs['method'] in validlist:
            raise Exception(kwargs['method']+" is not a valid option. Valid options are "+str(validlist))

        if kwargs['method'] == 'const':
            try:
                self.T[:] = kwargs['T']
                self.Told[:] = kwargs['T']
            except:
                raise Exception("'T' not specfied")

    def update_props(self):
        self.rho = self.fcns.rho(self.T)
        self.cp = self.fcns.cp(self.T)
        self.k = self.fcns.k(self.T)   
        self.alpha = self.k/(self.rho*self.cp)

        self.h = 20