import numpy as np

class Domain:
    """Domain class."""

    def add_input(self, **kwargs):
        """Add input to class.

        Args:
            kwargs (dict): Dictionary of arguments
        """

        for key, value in kwargs.items():
            setattr(self, key, value)

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

        return np.tile(self.H/(self.n[0]-1), (self.n[0],1))

    def node_pos(self):
        """Node position function."""

        return np.tile(np.linspace(0,self.H,self.n[0]), (1,1))

    def A(self):
        """Area of faces between nodes."""

        return (np.tile(np.pi*(self.D/2)**2, self.n[0]), np.tile(np.pi*(self.D/2)**2, self.n[0]))

    def V(self):
        """Volume of node element."""
        
        dx = self.H/(self.n[0]-1)
        face_pos_vec = np.concatenate(([0],np.linspace(dx/2,self.H-dx/2,self.n[0]-1),[self.H]))
        return np.tile(np.diff(np.pi*(self.D/2)**2*face_pos_vec), (1,1))

    def V0(self):
        """Volume of shape."""
        
        return np.pi*(self.D/2)**2*self.H