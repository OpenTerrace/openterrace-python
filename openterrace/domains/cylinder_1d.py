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

    def dx(self):
        """Node spacing function."""

        dx = self.H/(self.n-1)
        return np.repeat(dx, self.n)

    def node_pos(self):
        """Node position function."""

        return np.array(np.linspace(0,self.H,self.n))

    def A(self):
        """Area of faces between nodes."""

        return (np.repeat(np.pi*(self.D/2)**2, self.n), np.repeat(np.pi*(self.D/2)**2, self.n))

    def V(self):
        """Volume of node element."""
        
        dx = self.H/(self.n-1)
        face_pos_vec = np.concatenate(([0],np.linspace(dx/2,self.H-dx/2,self.n-1),[self.H]))
        return np.diff(np.pi*(self.D/2)**2*face_pos_vec)

    def V0(self):
        """Volume of shape."""
        
        return np.pi*(self.D/2)**2*self.H