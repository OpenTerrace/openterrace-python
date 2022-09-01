import numpy as np

def validate_input(vars, domain):
    required = ['ny','D','H']
    for var in required:
        if not var in vars:
            raise Exception("Keyword \'"+var+"\' not specified for domain of type \'"+domain+"\'")

def shape(vars):
    ny = vars['ny']
    return (1,ny,1)

def An(vars, shape):
    D = vars['D']
    return np.tile(np.pi*(D**2/4),shape)

def As(vars, shape):
    D = vars['D']
    return np.tile(np.pi*(D**2/4),shape)

def Aw(vars, shape):
    return np.tile(0,shape)

def Ae(vars, shape):
    return np.tile(0,shape)

def V(vars, shape):
    ny = vars.get('ny', 100)
    H = vars.get('H',None)
    D = vars.get('D',None)
    return np.pi*D**2/4*H/ny