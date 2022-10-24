import numpy as np

def validate_input(vars, domain_shape):
    required = ['n','D','H']
    for var in required:
        if not var in vars:
            raise Exception("Keyword \'"+var+"\' not specified for domain of type \'"+domain_shape+"\'")

def shape(vars):
    n = vars['n']
    return np.array([n])

def dx(vars):
    n = vars['n']
    H = vars['H']
    dx = H/(n-1)
    return np.repeat(dx, n)

def node_pos(vars):
    n = vars['n']
    H = vars['H']
    return np.array(np.linspace(0,H,n))

def A(vars):
    n = vars['n']
    D = vars['D']
    H = vars['H']
    return (np.repeat(np.pi*(D/2)**2, n), np.repeat(np.pi*(D/2)**2, n))

def V(vars):
    n = vars['n']
    D = vars['D']
    H = vars['H']
    dx = H/(n-1)
    face_pos_vec = np.concatenate(([0],np.linspace(dx/2,H-dx/2,n-1),[H]))
    return np.diff(np.pi*(D/2)**2*face_pos_vec)