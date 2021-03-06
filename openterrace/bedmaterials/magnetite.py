"""Data for Magnetite
"""

def rho(T):
    """Dummy function for constant density.

    Args:
        T (float): Temperature in kelvin

    Returns:
        float: Density in kg/m^3
    """
    return 5150*T**0

def k(T):
    """Dummy function for constant thermal conductivity.

    Args:
        T (float): Temperature in kelvin

    Returns:
        float: Thermal conductivity in W/(m K)
    """
    return 1.9*T**0

def cp(T):
    """Dummy function for constant specific heat capacity.

    Args:
        T (float): Temperature in kelvin

    Returns:
        float: Specific heat capacity in J/(kg K)
    """
    return 1130*T**0