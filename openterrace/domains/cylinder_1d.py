import numpy as np

class Domain:
    """Domain class."""
    def __init__(self, n:int, D:float, H:float):
        self.n = n
        self.D = D
        self.H = H

    def required_input(self):
        return ['n','D','H']

    def n_nodes(self):
        """n_nodes function.

        Args:
            vars (list): List of arguments
        """

        return np.array([self.n])

    def dx(vars):
        """Node spacing function.

        Args:
            vars (list): List of arguments
        """

        n = vars['n']
        H = vars['H']
        dx = H/(n-1)
        return np.repeat(dx, n)

    def node_pos(vars):
        """Node position function.

        Args:
            vars (list): List of arguments
        """

        n = vars['n']
        H = vars['H']
        return np.array(np.linspace(0,H,n))

    def A(vars):
        """Area of faces between nodes.

        Args:
            vars (list): List of arguments
        """

        n = vars['n']
        D = vars['D']
        H = vars['H']
        return (np.repeat(np.pi*(D/2)**2, n), np.repeat(np.pi*(D/2)**2, n))

    def V(vars):
        """Volume of node element.

        Args:
            vars (list): List of arguments
        """
        
        n = vars['n']
        D = vars['D']
        H = vars['H']
        dx = H/(n-1)
        face_pos_vec = np.concatenate(([0],np.linspace(dx/2,H-dx/2,n-1),[H]))
        return np.diff(np.pi*(D/2)**2*face_pos_vec)

    def V0(vars):
        """Volume of shape.

        Args:
            vars (list): List of arguments
        """
        
        D = vars['D']
        H = vars['H']
        return np.pi*(D/2)**2*H