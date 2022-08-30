import numpy as np

def validate_input(vars, domain):
    required = ['ny','D','H']
    for var in required:
        if not var in vars:
            raise Exception("Keyword \'"+var+"\' not specified for domain of type \'"+domain+"\'")

def shape(vars):
    ny = vars.get('ny', 100)
    return (1,ny,1)

def An(vars):
    D = vars.get('D',None)
    return np.diff

def As(X=None,Y=None,Z=None):
    return np.diff(X[1:,:],n=1,axis=1)

def Aw(X=None,Y=None,Z=None):
    return np.diff(X[1:,:],n=1,axis=1)

def Ae(X=None,Y=None,Z=None):
    return np.diff(X[1:,:],n=1,axis=1)

def V(X=None,Y=None,Z=None):
    return (X[1:,1:]-X[:-1,:-1])*(Y[1:,1:]-Y[:-1,:-1])