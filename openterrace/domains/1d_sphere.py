import numpy as np

def pos(args):
    """Returns a position vector as function of radius

    Args:
        r (float): Radius of sphere
        nx (float): Number of discretisations

    Returns:
        numpy.dtype: Position vector in sphere
    """
    return np.linspace(0,args.r,args.nx+1)

def pos_c(args):
    """Returns the node positions

    Args:
        pos (float): Position vector in sphere

    Returns:
        float: Node positions in sphere
    """
    return (args.pos[:-1]+args.pos[1:])/2

def Aw(args):
    """Returns the west surface area given a position vector pos

    Args:
        numpy.dtype: Radial position in sphere

    Returns:
        numpy.dtype: Surface area at position
    """
    return 4*np.pi*args.pos[:-1]**2

def Ae(args):
    """Returns the west surface area given a position vector pos

    Args:
        numpy.dtype: Radial position in sphere

    Returns:
        numpy.dtype: Surface area at position
    """
    return 4*np.pi*args.pos[1:]**2

def V(args):
    return np.diff(4/3*np.pi*args.pos**3, axis=0)