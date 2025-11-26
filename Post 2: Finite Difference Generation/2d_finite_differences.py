import numpy as np
from math import factorial, perm, ceil, sqrt, comb

def regular_forward_differencing(dx, dy, n, order=(1, 0)):
    # dx, dy = interval spacing
    # n = number of points to look in each direction. Total number 
    #     of points used is thus n**2

    x = [dx*i for i in range(n)]
    y = [dy*i for i in range(n)] 
    X = np.vander(x, increasing=True, N=ceil(sqrt(2)*n))
    Y = np.vander(y, increasing=True, N=ceil(sqrt(2)*n))
    A = np.zeros([n*n, n*n])
    b = np.zeros([n*n, 1])

    deriv_order = 0
    i = 0
    done = False
    while True:
        for j in range(0, deriv_order+1):
            if i+j < n*n:
                c = comb(deriv_order, j) / factorial(deriv_order)
                A[:, i+j] = [x*y for y in Y[:, j] for x in X[:, deriv_order -  j]] 
            else:
                done = True
                break
        if done:
            break
        else:
            deriv_order += 1
            i += deriv_order

    m = order[0] + order[1]
    b[(m-1)*m//2 + 1] = 1

    return A



def test_forward_differencing(dx, dy, n, order=(1, 0)):
    # dx, dy = interval spacing
    # n = number of points to look in each direction. Total number 
    #     of points used is thus n*(n+1)//2

    m = n*(n+1)//2
    x = [dx*i for i in range(n)]
    y = [dy*i for i in range(n)] 
    X = np.vander(x, increasing=True, N=n)
    Y = np.vander(y, increasing=True, N=n)
    A = np.zeros([m, m])
    b = np.zeros([m, 1])
    print(X)
    print(Y)

    for i in range(n):
        for j in range(i):
            for k in range(n):
                for l in range(k):
                    A[j, k+l] = X[,] * Y[]

    m = order[0] + order[1]
    b[(m-1)*m//2 + 1] = 1

    return A

np.set_printoptions(precision=3, suppress=True)
A = test_forward_differencing(1, 1, 2)
print(A)
B = np.linalg.inv(A)
print(B)
