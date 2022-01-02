# Data for water in the range 0 C to 95 C from VDI Waermeatlas. 
# Note: Temperature should be given in Kelvin

#Function for density
def rho(T):
    return -0.00365471*T**2 + 1.93017*T + 746.025

#Function for thermal conductivity
def k(T):
    return -9.29827e-6*T**2 + 0.0071857*T - 0.710696

#Function for specific heat capacity
def cp(T):
    return -0.000127063*T**3 + 0.13736*T**2 - 48.6714*T + 9850.69

#Function for dynamic viscosity
def mu(T):
    return -2.80572e-9*T**3 + 2.90283e-6*T**2 - 0.00100532*T + 0.116947