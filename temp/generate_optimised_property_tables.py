import CoolProp.CoolProp as CP
import numpy as np
import time
import fluids


T = 50+273.15
P = 101325

###
# substance = 'Water'
# fluid = CP.AbstractState('BICUBIC&HEOS', substance)
# fluid.update(CP.PT_INPUTS, P, T)
# H = fluid.keyed_output(CP.iHmass)
# t = time.time()
# for i in range(1000000):
#     fluid.update(CP.HmassP_INPUTS, H, P)
#     [fluid.keyed_output(k) for k in [CP.iT, CP.iDmass, CP.iCpmass, CP.iviscosity, CP.iconductivity]]
# elapsed = time.time() - t
# print("Coolprop low level:", elapsed)
###


t = time.time()
for i in range(1000000):
    fluid.update(CP.HmassP_INPUTS, H, P)
    [fluid.keyed_output(k) for k in [CP.iT, CP.iDmass, CP.iCpmass, CP.iviscosity, CP.iconductivity]]
elapsed = time.time() - t
print("Coolprop low level:", elapsed)