import numpy as np

class Domain:
    """Domain class."""

    def required_input(self):
        """List of required input."""

        return ['n','D','H']

    def update_parameters(self):
        """Update parameters."""

        self.dx = self.dx()
        self.node_pos = self.node_pos()
        self.A = self.A()
        self.V = self.V()
        self.V0 = self.V0()

    def dx(self):
        """Node spacing."""

        return np.tile(self.H/(self.n[0]-1), (self.n[0], 1))

    def node_pos(self):
        """Node position function."""

        return np.tile(np.linspace(0,self.H,self.n[0]), (self.n[1],1)).T

    def A(self):
        """Area of faces between nodes."""

        return (np.tile(np.pi*(self.D/2)**2, (self.n[0],1)), np.tile(np.pi*(self.D/2)**2, (self.n[0],1)))

    def V(self):
        """Volume of node element."""
        
        dx = self.H/(self.n[0]-1)
        return np.tile(dx*np.pi*self.D**2/4, (self.n[0],1))

    def V0(self):
        """Volume of shape."""
        
        return np.pi*(self.D/2)**2*self.H