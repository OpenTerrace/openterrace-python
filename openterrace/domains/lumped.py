import numpy as np

def validate_input(vars, domain_shape):
    """Validates input arguments.

    Args:
        vars (list): List of arguments
        domain_shape (str): Name of domain type
    """
        
    required = ['V','A']
    for var in required:
        if not var in vars:
            raise Exception("Keyword \'"+var+"\' not specified for domain of type \'"+domain_shape+"\'")

def shape(vars):
    """Shape function.

    Args:
        vars (list): List of arguments
    """
    n = 1
    return np.array([n])

def dx(vars):
    """Node spacing function.

    Args:
        vars (list): List of arguments
    """

    return np.repeat(0, 1)

def node_pos(vars):
    """Node position function.

    Args:
        vars (list): List of arguments
    """

    return np.array([0, 1])

def A(vars):
    """Cross-sectional area for faces of node.

    Args:
        vars (list): List of arguments
    """

    A = vars['A']
    return np.array([[0,0],[0,A]])

def V(vars):
    """Volume of node element.

    Args:
        vars (list): List of arguments
    """

    V = vars['V']
    return np.repeat(V,1)

def V0(vars):
    """Volume of shape.

    Args:
        vars (list): List of arguments
    """
    
    V = vars['V']    
    return V