import numpy as np
import sys

def validate_input(vars):
    if not 'ny' in vars:
        raise Exception("Keyword 'ny' not specified in ",sys.argv[0])

def shape(vars):
    ny = vars.get('ny', 100)
    return (None,ny,None)

def An(vars):
    D = vars.get('D',None)
    return 

def As(X=None,Y=None,Z=None):
    return np.diff(X[1:,:],n=1,axis=1)

def V(X=None,Y=None,Z=None):
    return (X[1:,1:]-X[:-1,:-1])*(Y[1:,1:]-Y[:-1,:-1])