def h(T: float) -> float:
    """Mass specific enthalpy as function of temperature at 1 atm (fit valid between 200 K to 2000 K).

    Reference: Eric W. Lemmon, Richard T. Jacobsen, Steven G. Penoncello, and Daniel G. Friend. Thermodynamic Properties of Air and Mixtures of Nitrogen, Argon, and Oxygen from 60 to 2000 K at Pressures to 2000 MPa. J. Phys. Chem. Ref. Data, 29(3):331–385, 2000. doi:10.1063/1.1285884.

    Args:
        T (float): Temperature in kelvin

    Returns:
        Specific enthalpy in J/kg
    """
    return 9.94069026e-02**T**2 + 9.36245621e+02*T + 1.36134443e+05

def T(h: float) -> float:
    """Temperature as function of enthalpy at 1 atm (fit valid between 200 K to 2000 K).

    Reference: Eric W. Lemmon, Richard T. Jacobsen, Steven G. Penoncello, and Daniel G. Friend. Thermodynamic Properties of Air and Mixtures of Nitrogen, Argon, and Oxygen from 60 to 2000 K at Pressures to 2000 MPa. J. Phys. Chem. Ref. Data, 29(3):331–385, 2000. doi:10.1063/1.1285884.

    Args:
        h (float): Specific enthalpy in J/kg

    Returns:
        Temperature in kelvin
    """
    return -8.46672403e-11**h**2 + 1.07323754e-03*h - 1.41828256e+02
       

def rho(T: float) -> float:
    """Density as function of temperature at 1 atm (fit valid between 200 K to 1000 K).

    Reference: Eric W. Lemmon, Richard T. Jacobsen, Steven G. Penoncello, and Daniel G. Friend. Thermodynamic Properties of Air and Mixtures of Nitrogen, Argon, and Oxygen from 60 to 2000 K at Pressures to 2000 MPa. J. Phys. Chem. Ref. Data, 29(3):331–385, 2000. doi:10.1063/1.1285884.

    Args:
        T (float): Temperature in kelvin

    Returns:
        Density in kg/m^3
    """
    return 1.03151050e-11*T**4 - 2.98588024e-08*T**3 + 3.27062840e-05*T**2 - 1.67954625e-02*T + 4.00725905e+00

def k(T: float) -> float:
    """Thermal conductivity as function of temperature at 1 atm (valid between 200 K to 1000 K).

    Reference: E. W. Lemmon and R. T Jacobsen. Viscosity and Thermal Conductivity Equations for Nitrogen, Oxygen, Argon, and Air. Int. J. Thermophys., 25(1):21–69, 2004. doi:10.1023/B:IJOT.0000022327.04529.f3.

    Args:
        T: Temperature in kelvin

    Returns:
        Thermal conductivity in W/(m K)
    """
    return -1.81458474e-08*T**2 + 8.21681514e-05*T + 3.28247609e-03

def cp(T: float) -> float:
    """Specific heat capacity as function of temperature at 1 atm (valid between 250 K to 1000 K).

    Reference: Eric W. Lemmon, Richard T. Jacobsen, Steven G. Penoncello, and Daniel G. Friend. Thermodynamic Properties of Air and Mixtures of Nitrogen, Argon, and Oxygen from 60 to 2000 K at Pressures to 2000 MPa. J. Phys. Chem. Ref. Data, 29(3):331–385, 2000. doi:10.1063/1.1285884.

    Args:
        T: Temperature in kelvin

    Returns:
        Specific heat capacity in J/(kg K)
    """
    return -3.77730090e-07*T**3 + 8.21136099e-04*T**2 - 3.51274993e-01*T + 1.04771399e+03

def mu(T: float) -> float:
    """Dynamic viscosity as function of temperature at 1 atm (valid between 250 K to 1000 K).

    Reference: E. W. Lemmon and R. T Jacobsen. Viscosity and Thermal Conductivity Equations for Nitrogen, Oxygen, Argon, and Air. Int. J. Thermophys., 25(1):21–69, 2004. doi:10.1023/B:IJOT.0000022327.04529.f3.

    Args:
        T: Temperature in kelvin

    Returns:
        Dynamic viscosity in kg/(m s)
    """
    return -1.52828802e-11*T**2 + 5.48760775e-08*T + 3.37830161e-06

def Pr(T: float) -> float:
    """Prandtl number as function of temperature at 1 atm (valid between 250 K to 1000 K).

    References:
    Eric W. Lemmon, Richard T. Jacobsen, Steven G. Penoncello, and Daniel G. Friend. Thermodynamic Properties of Air and Mixtures of Nitrogen, Argon, and Oxygen from 60 to 2000 K at Pressures to 2000 MPa. J. Phys. Chem. Ref. Data, 29(3):331–385, 2000. doi:10.1063/1.1285884.
    E. W. Lemmon and R. T Jacobsen. Viscosity and Thermal Conductivity Equations for Nitrogen, Oxygen, Argon, and Air. Int. J. Thermophys., 25(1):21–69, 2004. doi:10.1023/B:IJOT.0000022327.04529.f3.

    Args:
        T: Temperature in kelvin

    Returns:
        Prandtl number
    """
    return -3.44221157e-10*T**3 + 7.68746087e-07*T**2 - 4.91282964e-04*T + 7.94844297e-01