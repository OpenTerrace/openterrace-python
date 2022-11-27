import numpy as np

def validate_input(vars, domain_shape):
    required = ['n','A','L']
    for var in required:
        if not var in vars:
            raise Exception("Keyword \'"+var+"\' not specified for domain of type \'"+domain_shape+"\'")

def shape(vars):
    n = vars['n']
    return np.array([n])

def dx(vars):
    n = vars['n']
    L = vars['L']
    dx = L/(n-1)
    return np.repeat(dx, n)

def node_pos(vars):
    n = vars['n']
    L = vars['L']
    return np.array(np.linspace(0,L,n))

def A(vars):
    n = vars['n']
    A = vars['A']
    return (np.repeat(A,n), np.repeat(A,n))

def V(vars):
    n = vars['n']
    A = vars['A']
    L = vars['L']
    dx = L/(n-1)
    face_pos_vec = np.concatenate(([0], np.linspace(dx/2,L-dx/2,n-1), [L]))
    return np.diff(A*face_pos_vec)