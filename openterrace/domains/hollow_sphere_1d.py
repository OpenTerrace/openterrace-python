import numpy as np

def validate_input(vars, domain_shape):
    required = ['n','Rinner','Router']
    for var in required:
        if not var in vars:
            raise Exception("Keyword \'"+var+"\' not specified for domain of type \'"+domain_shape+"\'")

def shape(vars):
    n = vars['n']
    return np.array([n])

def dx(vars):
    n = vars['n']
    Rinner = vars['Rinner']
    Router = vars['Router']
    dx = (Router-Rinner)/(n-1)
    return np.repeat(dx, n)

def node_pos(vars):
    n = vars['n']
    Rinner = vars['Rinner']
    Router = vars['Router']
    return np.array(np.linspace(Rinner,Router,n))

def A(vars):
    n = vars['n']
    Rinner = vars['Rinner']
    Router = vars['Router']
    dx = (Router-Rinner)/(n-1)
    face_pos_vec = np.concatenate(([Rinner],np.linspace(Rinner+dx/2,Router-dx/2,n-1),[Router]))
    return np.array([(4*np.pi*face_pos_vec**2)[:-1], (4*np.pi*face_pos_vec**2)[1:]])

def V(vars):
    n = vars['n']
    Rinner = vars['Rinner']
    Router = vars['Router']
    dx = (Router-Rinner)/(n-1)
    face_pos_vec = np.concatenate(([Rinner],np.linspace(Rinner+dx/2,Router-dx/2,n-1),[Router]))
    return np.diff(4/3*np.pi*face_pos_vec**3)