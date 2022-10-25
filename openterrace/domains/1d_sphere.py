import numpy as np

def validate_input(vars, domain_shape):
    required = ['n','R']
    for var in required:
        if not var in vars:
            raise Exception("Keyword \'"+var+"\' not specified for domain of type \'"+domain_shape+"\'")

def shape(vars):
    n = vars['n']
    return np.array([n])

def dx(vars):
    n = vars['n']
    R = vars['R']
    dx = R/(n-1)
    return np.repeat(dx, n)

def node_pos(vars):
    n = vars['n']
    R = vars['R']
    return np.array(np.linspace(0,R,n))

def A(vars):
    n = vars['n']
    R = vars['R']
    dx = R/(n-1)
    face_pos_vec = np.concatenate(([0],np.linspace(dx/2,R-dx/2,n-1),[R]))
    return np.array([(4*np.pi*face_pos_vec**2)[:-1], (4*np.pi*face_pos_vec**2)[1:]])

def V(vars):
    n = vars['n']
    R = vars['R']
    dx = R/(n-1)
    face_pos_vec = np.concatenate(([0],np.linspace(dx/2,R-dx/2,n-1),[R]))
    return np.diff(4/3*np.pi*face_pos_vec**3)