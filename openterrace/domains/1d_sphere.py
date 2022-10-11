import numpy as np

def validate_input(vars, domain_shape):
    required = ['n','D']
    for var in required:
        if not var in vars:
            raise Exception("Keyword \'"+var+"\' not specified for domain of type \'"+domain_shape+"\'")

def shape(vars):
    n = vars['n']
    return np.array([n])

def dx(vars):
    n = vars['n']
    D = vars['D']
    return (np.repeat(D/2/n, n+2), np.repeat(D/2/n, n+2))

def A(vars):
    n = vars['n']
    D = vars['D']
    r_vec = np.arange(-(D/2)/n, D/2+2*(D/2)/n, (D/2)/n)
    return np.array([(4*np.pi*r_vec**2)[:-1], (4*np.pi*r_vec**2)[1:]])

def V(vars):
    n = vars['n']
    D = vars['D']
    r_vec = np.linspace(0-(D/2/n), D/2+(D/2/n), n+3)
    return np.diff(4/3*np.pi*r_vec**3)