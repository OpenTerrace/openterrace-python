"""Data for Swedish Diabase
"""

def rho(T):
    """Dummy function for constant density.

    Args:
        T (float): Temperature in kelvin

    Returns:
        float: Density in kg/m^3
    """
    return 3007*T**0

def k(T):
    """Dummy function for constant thermal conductivity.

    Args:
        T (float): Temperature in kelvin

    Returns:
        float: Thermal conductivity in W/(m K)
    """
    return 1.75*T**0

def cp(T):
    """Dummy function for constant specific heat capacity.

    Args:
        T (float): Temperature in kelvin

    Returns:
        float: Specific heat capacity in J/(kg K)
    """
    return 1272*T**0