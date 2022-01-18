import fluids
import solids
import shapes

class Properties():
    """The properties class stores functions that load function of thermophysical properties of the fluid and bed material. Also shape functions of the bed material are stored.
    """
    def select_fluid(self, fluid_type):
        try:
            self.fluid = getattr(fluids, fluid_type)
        except:
            raise Exception("Valid options for fluid are:",fluids.__all__)

    def select_solid(self, solid_type):
        try:
            self.solid = getattr(solids, solid_type)
        except:
            raise Exception("Valid options for solid are:",solids.__all__)

    def select_shape(self, shape):
        try:
            self.shape = getattr(shapes, shape)
        except:
            raise Exception("Valid options for shape are:",shapes.__all__)