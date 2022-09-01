import numpy as np

def validate_input(vars, domain_shape):
    required = ['n','D','H']
    for var in required:
        if not var in vars:
            raise Exception("Keyword \'"+var+"\' not specified for domain of type \'"+domain_shape+"\'")

def shape(vars):
    n = vars['n']
    return np.array([n])

def A(vars):
    D = vars['D']
    n = vars['n']
    return np.repeat(np.pi*(D**2/4), n+1)

def V(vars):
    n = vars['n']
    H = vars['H']
    D = vars['D']
    return np.repeat(np.pi*(D**2/4)*H/n, n)