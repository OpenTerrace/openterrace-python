# Data for air (1 atm) in the range 250 K to 1000 K. 
# Note: Temperature should be given in Kelvin
# See documentation for curve fitting

#Function for density
def rho(T):
    return 6.99321266968349e-12*T**4 - 2.13949101637962e-08*T**3 + 2.49556828014612e-05*T**2 - 0.0137812349600436*T + 3.57990616714300

#Function for thermal conductivity
def k(T):
    return -2.74159663865546e-08*T**2 + 9.26081932773110e-05*T + 0.00104196428571427

#Function for specific heat capacity
def cp(T):
    return -3.84827075229561e-07*T**3 + 0.000838847684822935*T**2 -0.364483701712815*T + 1050.66046054049

#Function for dynamic viscosity
def mu(T):
    return -1.58956582633054e-11*T**2 + 5.46339845938377e-08*T + 3.54058298319323e-06

#Function for Prandtl number
def Pr(T):
    return 9.30380249266224e-16*T**5 - 3.53814400254198e-12*T**4 + 4.52699055330845e-09*T**3 - 2.12904461379820e-06*T**2 + 0.000187441890926772*T + 0.747916944510558