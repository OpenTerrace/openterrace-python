import numpy as np

A = np.array([[[1,2,3],[1,3,5]]])#,[[1,4,7],[1,6,11]]])

for i in range(A.shape[0]):
    for j in range(A.shape[1]):
        for k in range(A.shape[2]):
            print(i,j,k)
            print(A[i,j,k])