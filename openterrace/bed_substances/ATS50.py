"""
Data for ATS50 phase change material.

Reference: https://www.axiotherm.de/en/download/project/productdatasheet/file/17/

T_s = 56+273.15 (solidification temperature)
T_l = 58+273.15 (liquid temperature)
k_s = 1 (solid thermal conductivity)
k_l = 0.6 (liquid thermal conductivity)
h_f = 240000 (latent heat of fusion)
cp = 3000 (specific heat capacity at constant pressure)
rho_l = 1280 (liquid density)
rho_s = 1280 (solid density)
h_s = T_s*cp (mass specific enthalpy before phase change)
h_l = T_s*cp+h_f (mass specific enthalpy at after phase change)
"""

import numpy as np

_T_s = 49+273.15 #Solidification temperature
_T_l = 50+273.15 #Liquid temperature
_k_s = 1 #Solid thermal conductivity
_k_l = 0.6 #Liquid thermal conductivity
_h_f = 228000 #Latent heat of phase shift
_cp = 3000 #Specific heat capacity
_rho_l = 1300 #Liquid density
_rho_s = _rho_l #Solid density
_h_s = _T_s*_cp #Mass specific enthalpy at point of solidification
_h_l = _h_s+_h_f #Mass specific enthalpy after phase shift

def h(T:float) -> float:
    """Mass specific enthalpy as function of temperature at 1 atm (fit assumes piecewice constant cp with phase change).

    Args:
        T (float): Temperature in K

    Returns:
        Specific enthalpy in J/kg
    """
    return np.piecewise(T, [T <= _T_s, (T > _T_s) & (T <= _T_l), T > _T_l], [lambda T: _cp*T, lambda T: _h_s + (T-_T_s)/(_T_l-_T_s)*_h_f, lambda T: _h_l + _cp*(T-_T_l)])

def T(h:float, p:float=None) -> float:
    """Temperature as function of mass specific enthalpy at 1 atm (fit assumes piecewice constant cp with phase change).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        Temperature in kelvin
    """
    return np.piecewise(h, [h <= _h_s, (h > _h_s) & (h <= _h_l), h > _h_l], [lambda h: 1/_cp*h, lambda h: _T_s + (_T_l-_T_s)*(h-_h_s)/(_h_l-_h_s), lambda h: _T_l + 1/_cp*(h-_h_l)])


def rho(h:float, p:float=None) -> float:
    """Density as function of mass specific entahlpy at 1 atm (fit assumes constant density).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        float: Density in kg/m^3
    """
    return _rho_l*h**0

def k(h:float, p:float=None) -> float:
    """Thermal conductivity as function of mass specific enthalpy at 1 atm (fit assumes piecewice constant k).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        float: Thermal conductivity in W/(m K)
    """
    return np.piecewise(h, [h <= _h_s, (h > _h_s) & (h <= _h_l), h > _h_l], [_k_s, lambda h: _k_s + (_k_l-_k_s)/(_h_l-_h_s)*(h-_h_s), _k_l])

def cp(h:float, p:float=None) -> float:
    """Specific heat capacity as function of mass specific enthalpy at 1 atm (fit assumes piecewice constant cp with phase change).

    Args:
        h (float): Specific enthalpy in J/kg
        p (float): Pressure in Pa

    Returns:
        float: Specific heat capacity in J/(kg K)
    """
    return _cp*h**0