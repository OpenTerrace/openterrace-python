import fluids
import solids

class Fluid():
    def select(self, fluid_type):
        try:
            self.fluid_type = getattr(fluids, fluid_type)
        except:
            raise Exception("Valid options for fluid are:",fluids.__all__)

class Solid():
    def select(self, solid_type):
        try:
            self.solid_type = getattr(solids, solid_type)
        except:
            raise Exception("Valid options for solid are:",solids.__all__)