"""
Data for water.

Reference 1: W. Wagner and A. Pruß. The IAPWS Formulation 1995 for the Thermodynamic Properties of Ordinary Water Substance for General and Scientific Use. J. Phys. Chem. Ref. Data, 31:387–535, 2002. doi:10.1063/1.1461829.
Reference 2: M. L. Huber, R. A. Perkins, D. G. Friend, J. V. Sengers, M. J. Assael, I. N. Metaxa, K. Miyagawa, R. Hellmann, and E. Vogel. New International Formulation for the Thermal Conductivity of H2O. J. Phys. Chem. Ref. Data, 41(3):033102–1:23, 2012. doi:10.1063/1.4738955.
Reference 3: M. L. Huber, R. A. Perkins, A. Laesecke, D. G. Friend, J. V. Sengers, M. J Assael, I. M. Metaxa, E. Vogel, R. Mareš, and K. Miyagawa. New International Formulation for the Viscosity of H2O. J. Phys. Chem. Ref. Data, 38(2):101–125, 2009. doi:10.1063/1.3088050.
"""

def h(T: float) -> float:
    """Mass specific enthalpy as function of temperature at 1 atm (fit valid between 273 K to 373 K).

    Args:
        T (float): Temperature in K

    Returns:
        Specific enthalpy in J/kg
    """
    return 4186.56437769*T - 1143381.31556279

def T(h: float, p:float=None) -> float:
    """Temperature as function of mass specific enthalpy at 1 atm (fit valid between 273 K to 373 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Temperature in kelvin
    """
    return -1.16571910e-12*h**2 + 2.39343432e-04*h + 2.73074072e+02     

def rho(h: float, p:float=None) -> float:
    """Density as function of mass specific enthalpy at 1 atm (fit valid between 273 K to 373 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Density in kg/m^3
    """
    return 2.48881337e-16*h**3 - 3.55685672e-10*h**2 + 7.09888943e-06*h + 9.99916857e+02

def k(h: float, p:float=None) -> float:
    """Thermal conductivity as function of mass specific enthalpy at 1 atm (fit valid between 273 K to 373 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Thermal conductivity in W/(m K)
    """
    return -5.78946472e-13*h**2 + 5.22719636e-07*h + 5.57043098e-01

def cp(h: float, p:float=None) -> float:
    """Specific heat capacity as function of mass specific enthalpy at 1 atm (fit valid between 273 K to 373 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Specific heat capacity in J/(kg K)
    """
    return 9.12725636e-21*h**4 - 9.49490894e-15*h**3 + 3.98071678e-09*h**2 - 6.75046221e-04*h + 4.21790304e+03    

def mu(h: float, p:float=None) -> float:
    """Dynamic viscosity as function of mass specific enthalpy at 1 atm (fit valid between 273 K to 373 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Dynamic viscosity in kg/(m*s)
    """
    return -3.39233531e-20*h**3 + 3.17381373e-14*h**2 - 1.08887320e-08*h + 1.73113017e-03

def Pr(h: float, p:float=None) -> float:
    """Prandtl number as function of mass specific enthalpy at 1 atm (fit valid between 273 K to 373 K).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Prandtl number
    """
    return -3.02544350e-16*h**3 + 2.76464299e-10*h**2 - 9.03954950e-05*h + 1.30070174e+01