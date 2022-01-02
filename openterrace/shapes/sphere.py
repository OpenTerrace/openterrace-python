import numpy as np

def area(r):
    return 4*np.pi*r**2

def vol(r):
    return 4/3*pi*r**3

def volElement(rArr):
    return np.diff(4/3*np.pi*self.rFace**3)

# Function for Nusselt number as function of Reynolds number, Prandtl number, 
# dynamic viscosity at free stream temperature and dynamic visocity at surface
# temperature by:

# Whitaker S. Forced convection heat transfer correlations for flow in pipes, 
# past flat plates, single cylinders, single spheres, and flow in packed beds 
# and tube bundles. AIChE J 18, 361–371 (1972). 
def Nu(**kwargs):
    return 2 + (0.4*Re**(1/2) + 0.06*Re**(2/3)) * Pr**0.4 * (mu/mus)**(1/4)