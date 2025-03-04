import numpy as np

class Domain:
    """Domain class."""

    def required_input(self):
        """List of required input."""

        return ['n','area','length']

    def update_parameters(self):
        """Update parameters."""
        
        self.dx = self.dx_fcn()
        self.node_pos = self.node_pos_fcn()
        self.A = self.A_fcn()
        self.V = self.V_fcn()
        self.V0 = self.V0_fcn()

    def dx_fcn(self):
        """Node spacing function."""

        return np.tile(self.length/(self.n[0]-1), (self.n[0], 1))

    def node_pos_fcn(self):
        """Node position function."""

        return np.tile(np.linspace(0,self.length,self.n[0]), (self.n[1],1)).T

    def A_fcn(self):
        """Area of faces between nodes."""

        return (np.tile(self.area, (self.n[0],1)), np.tile(self.area, (self.n[0],1)))

    def V_fcn(self):
        """Volume of node element."""

        dx = self.length/(self.n[0]-1)
        return np.tile(dx*self.area, (self.n[0],1))

    def V0_fcn(self):
        """Volume of shape."""
            
        return self.area*self.length