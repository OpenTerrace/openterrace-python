"""Data for AXIOTHERM ATS 58 Phase Change Material (PCM)

h_if = 240000 J/kg (specific latent heat of fusion)

T_s = 56 C (melting temperature)

T_l = 58 C (liquid temperature)

k_s = 1 W/(m K) (thermal conductivity in solid state)

k_l = 0.6 W/(m K) (thermal conductivity in liquid state)
"""

h_if = 240000
T_s = 56+273.15
T_l = 58+273.15
k_s = 1
k_l = 0.6

import numpy as np

def rho(T):
    """Function for constant density.

    Args:
        T (float): Temperature in kelvin

    Returns:
        float: Density in kg/m^3
    """
    return 1280*T**0

def k(T):
    """Piece-wise function for thermal conductivity.

    Args:
        T (float): Temperature in kelvin

    Returns:
        float: Thermal conductivity in W/(m K)
    """
    return np.piecewise(T, [T <= T_s, (T > T_s) & (T <= T_l), T > T_l], [k_s, lambda T: (k_l-k_s)/(T_l-T_s)*(T-T_s)+k_s, k_l])

def cp(T):
    """Function for constant specific heat capacity.

    Args:
        T (float): Temperature in kelvin

    Returns:
        float: Specific heat capacity in J/(kg K)
    """
    return 3000*T**0