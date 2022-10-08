def h(T: float) -> float:
    """Mass specific enthalpy as function of temperature at 1 atm (fit valid between 273.15 K to 2000 K).

    Reference: Eric W. Lemmon, Richard T. Jacobsen, Steven G. Penoncello, and Daniel G. Friend. Thermodynamic Properties of Air and Mixtures of Nitrogen, Argon, and Oxygen from 60 to 2000 K at Pressures to 2000 MPa. J. Phys. Chem. Ref. Data, 29(3):331–385, 2000. doi:10.1063/1.1285884.

    Args:
        T (float): Temperature in K

    Returns:
        Mass specific enthalpy in J/kg
    """
    return 1.06401974e-01*T**2 + 9.26624243e+02*T + 1.39199143e+05
  
def T(h: float, p:float=None) -> float:
    """Temperature as function of mass specific enthalpy at 1 atm (fit valid between 273.15 K to 1000 K).

    Reference: Eric W. Lemmon, Richard T. Jacobsen, Steven G. Penoncello, and Daniel G. Friend. Thermodynamic Properties of Air and Mixtures of Nitrogen, Argon, and Oxygen from 60 to 2000 K at Pressures to 2000 MPa. J. Phys. Chem. Ref. Data, 29(3):331–385, 2000. doi:10.1063/1.1285884.

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Temperature in kelvin
    """
    return -8.46672403e-11*h**2 + 1.07323754e-03*h - 1.41828256e+02

def rho(h: float, p:float=None) -> float:
    """Density as function of mass specific enthalpy at 1 atm (fit valid between 273.15 K to 1000 K).

    Reference: Eric W. Lemmon, Richard T. Jacobsen, Steven G. Penoncello, and Daniel G. Friend. Thermodynamic Properties of Air and Mixtures of Nitrogen, Argon, and Oxygen from 60 to 2000 K at Pressures to 2000 MPa. J. Phys. Chem. Ref. Data, 29(3):331–385, 2000. doi:10.1063/1.1285884.

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Density in kg/m^3
    """
    return -3.07491951e-18*h**3 - 8.99511511e-12*h**2 - 9.18059393e-06*h + 3.68623992e+00

def k(h: float, p:float=None) -> float:
    """Thermal conductivity as function of mass specific enthalpy at 1 atm (fit valid between 273.15 K to 1000 K).

    Reference: E. W. Lemmon and R. T Jacobsen. Viscosity and Thermal Conductivity Equations for Nitrogen, Oxygen, Argon, and Air. Int. J. Thermophys., 25(1):21–69, 2004. doi:10.1023/B:IJOT.0000022327.04529.f3.

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Thermal conductivity in W/(m K)
    """
    return -1.93368179e-14*h**2 + 8.56084207e-08*h - 6.41427790e-03
    

def cp(h: float, p:float=None) -> float:
    """Specific heat capacity as function of mass specific enthalpy at 1 atm (fit valid between 273.15 K to 1000 K).

    Reference: Eric W. Lemmon, Richard T. Jacobsen, Steven G. Penoncello, and Daniel G. Friend. Thermodynamic Properties of Air and Mixtures of Nitrogen, Argon, and Oxygen from 60 to 2000 K at Pressures to 2000 MPa. J. Phys. Chem. Ref. Data, 29(3):331–385, 2000. doi:10.1063/1.1285884.

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Specific heat capacity in J/(kg K)
    """
    return -3.34421271e-16*h**3 + 8.54646323e-10*h**2 - 4.99992844e-04*h + 1.08968460e+03

def mu(h: float, p:float=None) -> float:
    """Dynamic viscosity as function of mass specific enthalpy at 1 atm (fit valid between 273.15 K to 1000 K).

    Reference: E. W. Lemmon and R. T Jacobsen. Viscosity and Thermal Conductivity Equations for Nitrogen, Oxygen, Argon, and Air. Int. J. Thermophys., 25(1):21–69, 2004. doi:10.1023/B:IJOT.0000022327.04529.f3.

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Dynamic viscosity in kg/(m*s)
    """
    return -1.50291961e-17*h**2 + 5.66505123e-11*h - 2.72708492e-06

def Pr(h: float, p:float=None) -> float:
    """Dynamic viscosity as function of mass specific enthalpy at 1 atm (fit valid between 273.15 K to 1000 K).

    References:
    Eric W. Lemmon, Richard T. Jacobsen, Steven G. Penoncello, and Daniel G. Friend. Thermodynamic Properties of Air and Mixtures of Nitrogen, Argon, and Oxygen from 60 to 2000 K at Pressures to 2000 MPa. J. Phys. Chem. Ref. Data, 29(3):331–385, 2000. doi:10.1063/1.1285884.
    E. W. Lemmon and R. T Jacobsen. Viscosity and Thermal Conductivity Equations for Nitrogen, Oxygen, Argon, and Air. Int. J. Thermophys., 25(1):21–69, 2004. doi:10.1023/B:IJOT.0000022327.04529.f3.

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Prandtl number
    """
    return 2.71884293e-25*h**4 - 1.12907428e-18*h**3 + 1.70869490e-12*h**2 - 1.05637297e-06*h + 9.25357206e-01
    