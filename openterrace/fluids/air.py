def rho(T: float) -> float:
    """Density as function of temperature at 1 atm (valid between 250 K to 1000 K).

    Args:
        T (float): Temperature in kelvin

    Returns:
        Density in kg/m^3
    """

    return 6.99321266968349e-12*T**4 - 2.13949101637962e-08*T**3 + 2.49556828014612e-05*T**2 - 0.0137812349600436*T + 3.57990616714300

def k(T: float) -> float:
    """Thermal conductivity as function of temperature at 1 atm (valid between 250 K to 1000 K).

    Args:
        T: Temperature in kelvin

    Returns:
        Thermal conductivity in W/(m K)
    """

    return -2.74159663865546e-08*T**2 + 9.26081932773110e-05*T + 0.00104196428571427

def cp(T: float) -> float:
    """Specific heat capacity as function of temperature at 1 atm (valid between 250 K to 1000 K).

    Args:
        T: Temperature in kelvin

    Returns:
        float: Specific heat capacity in J/(kg K)
    """
    return -3.84827075229561e-07*T**3 + 0.000838847684822935*T**2 -0.364483701712815*T + 1050.66046054049

def mu(T: float) -> float:
    """Dynamic viscosity as function of temperature at 1 atm (valid between 250 K to 1000 K).

    Args:
        T: Temperature in kelvin

    Returns:
        Dynamic viscosity in kg/(m s)
    """
    return -1.58956582633054e-11*T**2 + 5.46339845938377e-08*T + 3.54058298319323e-06

def Pr(T: float) -> float:
    """Prandtl number as function of temperature at 1 atm (valid between 250 K to 1000 K).

    Args:
        T): Temperature in kelvin

    Returns:
        Prandtl number
    """
    return 9.30380249266224e-16*T**5 - 3.53814400254198e-12*T**4 + 4.52699055330845e-09*T**3 - 2.12904461379820e-06*T**2 + 0.000187441890926772*T + 0.747916944510558