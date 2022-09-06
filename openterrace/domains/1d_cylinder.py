import numpy as np

def validate_input(vars, domain_shape):
    required = ['n','D','H']
    for var in required:
        if not var in vars:
            raise Exception("Keyword \'"+var+"\' not specified for domain of type \'"+domain_shape+"\'")

def shape(vars):
    n = vars['n']
    return np.array([n])

def Aw(vars):
    n = vars['n']
    D = vars['D']
    H = vars['H']
    return np.repeat(np.pi*D*H/2/n, n)

def Ae(vars):
    n = vars['n']
    D = vars['D']  
    H = vars['H']
    return np.repeat(np.pi*D*H/2/n, n)

def An(vars):
    n = vars['n']
    D = vars['D']  
    return np.repeat(np.pi*D**2/4, n)

def As(vars):
    n = vars['n']
    D = vars['D']  
    return np.repeat(np.pi*D**2/4, n)

def V(vars):
    n = vars['n']
    D = vars['D']
    H = vars['H']
    return np.repeat(np.pi*(D**2/4)*H/n, n)