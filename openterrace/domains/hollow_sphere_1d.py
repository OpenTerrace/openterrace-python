import numpy as np

class Domain:
    """Domain class."""

    def required_input(self):
            """List of required input."""

            return ['n','radius_inner','radius_outer']

    def update_parameters(self):
        """Update parameters."""
        
        self.dx = self.dx_fcn()
        self.node_pos = self.node_pos_fcn()
        self.A = self.A_fcn()
        self.V = self.V_fcn()
        self.V0 = self.V0_fcn()

    def dx_fcn(self):
        """Node spacing function."""

        return np.tile((self.radius_outer-self.radius_inner)/(self.n[0]-1), (self.n[0], 1))

    def node_pos_fcn(self):
        """Node position function."""

        return np.tile(np.linspace(self.radius_inner,self.radius_outer,self.n[0]), (self.n[1],1)).T

    def A_fcn(self):
        """Area of faces between nodes."""

        dx = (self.radius_outer-self.radius_inner)/(self.n[0]-1)
        face_pos_vec = np.concatenate(([self.radius_inner],np.linspace(self.radius_inner+dx/2,self.radius_outer-dx/2,self.n[0]-1),[self.radius_outer]))
        return (np.tile(4*np.pi*face_pos_vec[:-1]**2, (1,1)).T, np.tile(4*np.pi*face_pos_vec[1:]**2, (1,1)).T)

    def V_fcn(self):
        """Volume of node element."""

        dx = (self.radius_outer-self.radius_inner)/(self.n[0]-1)
        face_pos_vec = np.concatenate(([self.radius_inner],np.linspace(self.radius_inner+dx/2,self.radius_outer-dx/2,self.n[0]-1),[self.radius_outer]))
        return np.tile(np.diff(4/3*np.pi*face_pos_vec**3), (1,1)).T

    def V0_fcn(self):
        """Volume of shape."""
            
        return 4/3*np.pi*self.radius_outer**3