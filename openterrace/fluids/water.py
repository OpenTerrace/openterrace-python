def rho(T: float) -> float:
    """Density as function of temperature in K at 1 atm (valid between 273.15 K to 363.15 K).

    Args:
        T: Temperature in kelvin

    Returns:
        Density in kg/m^3
    """

    return -0.00365471*T**2 + 1.93017*T + 746.025

def k(T):
    """Thermal conductivity as function of temperature in K at 1 atm (valid between 273.15 K to 363.15 K).

    Args:
        T (float): Temperature in kelvin

    Returns:
        float: Thermal conductivity in W/(m K)
    """
    return -9.29827e-6*T**2 + 0.0071857*T - 0.710696

def cp(T):
    """Specific heat capacity as function of temperature in K at 1 atm (valid between 273.15 K to 363.15 K).
        
    Args:
        T (float): Temperature in kelvin

    Returns:
        (float): Specific heat capacity in J/(kg K)
    """
    return -0.000127063*T**3 + 0.13736*T**2 - 48.6714*T + 9850.69

def mu(T):
    """Dynamic viscosity as function of temperature in K at 1 atm (valid between 273.15 K to 363.15 K).

    Args:
        T (float): Temperature in kelvin

    Returns:
        float: Dynamic viscosity in kg/(m s)
    """
    return -2.80572e-9*T**3 + 2.90283e-6*T**2 - 0.00100532*T + 0.116947