"""
Data for liquid mixture of sodium (22%) and potassium (78%).

Reference 1: https://www-pub.iaea.org/MTCD/publications/PDF/IAEA-THPH_web.pdf
"""

def h(T:float) -> float:
    """Mass specific enthalpy as function of temperature at 1 atm (fit valid between 473.15 K to 873.15 K).

    Args:
        T (float): Temperature in K

    Returns:
        Specific enthalpy in J/kg
    """
    return 880.390075624882e+000*T - 227.268561225071e+003

def T(h:float, p:float=None) -> float:
    """Temperature as function of mass specific enthalpy at 1 atm (fit valid between 273 K to 373 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Temperature in kelvin
    """
    return 1.13586014618602e-003*h + 258.145301176596e+000

def rho(h:float, p:float=None) -> float:
    """Density as function of mass specific enthalpy at 1 atm (fit valid between 273 K to 373 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Density in kg/m^3
    """
    return -267.073587305967e-006*h + 868.620522246425e+000

def k(h:float, p:float=None) -> float:
    """Thermal conductivity as function of mass specific enthalpy at 1 atm (fit valid between 273 K to 373 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Thermal conductivity in W/(m K)
    """
    return -26.2590503127977e-012*h**2 + 21.6513924586817e-006*h + 21.5505803714445e+000

def cp(h:float, p:float=None) -> float:
    """Specific heat capacity as function of mass specific enthalpy at 1 atm (fit valid between 273 K to 373 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Specific heat capacity in J/(kg K)
    """
    return 474.869992698948e-012*h**2 - 455.554064632647e-006*h**1 + 980.401559485058e+000

def mu(h:float, p:float=None) -> float:
    """Dynamic viscosity as function of mass specific enthalpy at 1 atm (fit valid between 273 K to 373 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Dynamic viscosity in kg/(m*s)
    """
    return -2.72327193790784e-021*h**3 + 4.15934757530690e-015*h**2 - 2.31891771547815e-009*h + 625.420290036714e-006

def Pr(h:float, p:float=None) -> float:
    """Prandtl number as function of mass specific enthalpy at 1 atm (fit valid between 273 K to 373 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Prandtl number
    """
    return -125.757554730265e-021*h**3 + 193.669437204884e-015*h**2 - 105.180849961483e-009*h + 25.4815572990799e-003