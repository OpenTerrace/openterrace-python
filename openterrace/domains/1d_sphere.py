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
    dx = (D/2)/(n-1)
    return np.repeat(dx, n)

def node_pos(vars):
    n = vars['n']
    D = vars['D']
    return np.array(np.linspace(0,D/2,n))

def A(vars):
    n = vars['n']
    D = vars['D']
    dx = (D/2)/(n-1)
    face_pos_vec = np.concatenate(([0],np.linspace(dx/2,D/2-dx/2,n-1),[D/2]))
    return np.array([(4*np.pi*face_pos_vec**2)[:-1], (4*np.pi*face_pos_vec**2)[1:]])

def V(vars):
    n = vars['n']
    D = vars['D']
    dx = (D/2)/(n-1)
    face_pos_vec = np.concatenate(([0],np.linspace(dx/2,D/2-dx/2,n-1),[D/2]))
    return np.diff(4/3*np.pi*face_pos_vec**3)