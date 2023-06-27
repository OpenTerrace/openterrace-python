"""
Data for atmospheric air.

Reference 1: Eric W. Lemmon, Richard T. Jacobsen, Steven G. Penoncello, and Daniel G. Friend. Thermodynamic Properties of Air and Mixtures of Nitrogen, Argon, and Oxygen from 60 to 2000 K at Pressures to 2000 MPa. J. Phys. Chem. Ref. Data, 29(3):331–385, 2000. doi:10.1063/1.1285884.
Reference 2: E. W. Lemmon and R. T Jacobsen. Viscosity and Thermal Conductivity Equations for Nitrogen, Oxygen, Argon, and Air. Int. J. Thermophys., 25(1):21–69, 2004. doi:10.1023/B:IJOT.0000022327.04529.f3.
"""

def h(T:float) -> float:
    """Mass specific enthalpy as function of temperature at 1 atm (fit valid between 273.15 K to 1000 K).

    Args:
        T (float): Temperature in K

    Returns:
        Mass specific enthalpy in J/kg
    """
    return 1062.3436205*T + 100613.952812
  
def T(h:float, p:float=None) -> float:
    """Temperature as function of mass specific enthalpy at 1 atm (fit valid between 273.15 K to 1000 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Temperature in kelvin
    """
    return 9.41315014e-04*h - 9.47094244e+01

def rho(h:float, p:float=None) -> float:
    """Density as function of mass specific enthalpy at 1 atm (fit valid between 273.15 K to 1000 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Density in kg/m^3
    """
    return -2.99101902e-18*h**3 + 8.99511511e-12*h**2 - 9.18059393e-06*h + 3.68623992e+00

def k(h:float, p:float=None) -> float:
    """Thermal conductivity as function of mass specific enthalpy at 1 atm (fit valid between 273.15 K to 1000 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Thermal conductivity in W/(m K)
    """
    return -1.91985865e-14*h**2 + 8.53813872e-08*h - 6.32545058e-03
    

def cp(h:float, p:float=None) -> float:
    """Specific heat capacity as function of mass specific enthalpy at 1 atm (fit valid between 273.15 K to 1000 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Specific heat capacity in J/(kg K)
    """
    return -3.31926950e-16*h**3 + 8.48767643e-10*h**2 - 4.95535470e-04*h + 1.08860162e+03

def mu(h:float, p:float=None) -> float:
    """Dynamic viscosity as function of mass specific enthalpy at 1 atm (fit valid between 273.15 K to 1000 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Dynamic viscosity in kg/(m s)
    """
    return -1.49118910e-17*h**2 + 5.64575734e-11*h - 2.65149023e-06

def Pr(h:float, p:float=None) -> float:
    """Dynamic viscosity as function of mass specific enthalpy at 1 atm (fit valid between 273.15 K to 1000 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Prandtl number
    """
    return 2.71884293e-25*h**4 - 1.12907428e-18*h**3 + 1.70869490e-12*h**2 - 1.05637297e-06*h + 9.25357206e-01
    