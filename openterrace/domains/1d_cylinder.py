import numpy as np

def shape(nx=1, ny=None):
    return (ny,nx)

def Aw(X=None,Y=None,Z=None):
    return np.diff(Y[:,:-1],n=1,axis=0)

def Ae(X=None,Y=None,Z=None):
    return np.diff(Y[:,1:],n=1,axis=0)

def An(X=None,Y=None,Z=None):
    return np.diff(X[:-1,:],n=1,axis=1)

def As(X=None,Y=None,Z=None):
    return np.diff(X[1:,:],n=1,axis=1)

def V(X=None,Y=None,Z=None):
    return (X[1:,1:]-X[:-1,:-1])*(Y[1:,1:]-Y[:-1,:-1])