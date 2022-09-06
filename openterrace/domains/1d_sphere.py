import numpy as np

def validate_input(vars, domain_shape):
    required = ['n','D']
    for var in required:
        if not var in vars:
            raise Exception("Keyword \'"+var+"\' not specified for domain of type \'"+domain_shape+"\'")

def shape(vars):
    n = vars['n']
    return np.array([n])

def Aw(vars):
    D = vars['D']
    n = vars['n']
    r_vec = np.linspace(0,D/2,n+1)[:-1]
    return 4*np.pi*r_vec**2

def Ae(vars):
    D = vars['D']
    n = vars['n']
    r_vec = np.linspace(0,D/2,n+1)[1:]
    return 4*np.pi*r_vec**2

def V(vars):
    n = vars['n']
    D = vars['D']
    r_vec = np.linspace(0,D/2,n+1)
    return np.diff(4/3*np.pi*r_vec**3)