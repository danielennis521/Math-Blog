import numpy as np
from math import factorial, perm, ceil, sqrt

def regular_forward_differencing(dx, dy, n, order=1):
    # dx, dy = interval spacing
    # n = number of points to look in each direction. Total number 
    #     of points used is thus n**2

    x = [dx*i + 1 for i in range(n)]
    y = [dy*i + 2 for i in range(n)] 
    X = np.vander(x, increasing=True, N=ceil(sqrt(2)*n))
    Y = np.vander(y, increasing=True, N=ceil(sqrt(2)*n))
    A = np.zeros([n*n, n*n])

    deriv_order = 0
    i = 0
    done = False
    while True:
        for j in range(0, deriv_order+1):
            if i+j < n*n:
                c = perm(deriv_order, j) / factorial(deriv_order)
                A[:, i+j] = [x*y / c for y in Y[:, j] for x in X[:, deriv_order -  j]] 
            else:
                done = True
                break
        if done:
            break
        else:
            deriv_order += 1
            i += deriv_order

        

    return A


print(regular_forward_differencing(1, 1, 3))