from __future__ import print_function, division
import CoolProp.CoolProp as CP
import numpy as np
import timeit
import sys

T = 50+273.15
P = 101325

substance = 'Water'
fluid = CoolProp.AbstractState('BICUBIC&HEOS', substance)
fluid.update(CoolProp.PT_INPUTS, P, T)
H = fluid.keyed_output(CoolProp.iHmass)
print(H)

fluid.update(CoolProp.HmassP_INPUTS, H, P)
print([fluid.keyed_output(k) for k in [CoolProp.iT, CoolProp.iDmass, CoolProp.iCpmass, CoolProp.iviscosity, CoolProp.iconductivity]])
