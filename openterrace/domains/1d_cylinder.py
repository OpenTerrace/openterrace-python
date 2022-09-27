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
    n = vars['n']
    D = vars['D']
    H = vars['H']
    return (np.repeat(np.pi*(D/2)**2, n+2), np.repeat(np.pi*(D/2)**2, n+2))

def V(vars):
    n = vars['n']
    D = vars['D']
    H = vars['H']
    return (np.repeat(np.pi*(D/2)**2*H/n, n+2))