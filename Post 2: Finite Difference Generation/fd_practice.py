import numpy as np
from math import factorial


# simplest possible approach

def regular_forward_differencing(dx, n, order=1):
    # dx = interval spacing
    # n = number of points used in approximation

    A = np.vander([dx*i for i in range( n)], increasing=True)
    f = np.array([factorial(i) for i in range(n)])
    A = A/f
    B = np.linalg.inv(A)
    return B[order]


def nonregular_forward_differencing(x, order=1):
    # x = list of points to be used in the derivative approximation

    n = len(x)
    delta_x = np.array(x) - x[0]

    A = np.vander(delta_x, increasing=True)
    f = np.array([factorial(i) for i in range(n)])
    A = A/f
    B = np.linalg.inv(A)
    return B[order]


# faster / avoid direct inverse

def fast_rfd(dx, n, order=1):
    # dx = interval spacing
    # n = number of points used in approximation

    A = np.vander([dx*i for i in range( n)], increasing=True)
    f = np.array([factorial(i) for i in range(n)])
    A = A/f
    b = np.zeros(n)
    b[order] = 1
    return np.linalg.solve(A.T, b)


def fast_nfd(x, order=1):
    # x = list of points to be used in the derivative approximation

    n = len(x)
    delta_x = np.array(x) - x[0]

    A = np.vander(delta_x, increasing=True)
    f = np.array([factorial(i) for i in range(n)])
    A = A/f
    b = np.zeros(n)
    b[order] = 1
    return np.linalg.solve(A.T, b)


# avoid writing the same code multiple times

def forward_fd(dx=None, n=None, order=1, x=None):
    # x = list of points to be used in the derivative approximation
    # dx = interval spacing
    # n = number of points used in approximation

    if x != None:
        n = len(x)
        delta_x = np.array(x) - x[0]
    elif dx != None and n!=None:
        delta_x = [dx*i for i in range( n)]
    else:
        raise Exception('specify x or dx and n')

    A = np.vander(delta_x, increasing=True)
    f = np.array([factorial(i) for i in range(n)])
    A = A/f
    b = np.zeros(n)
    b[order] = 1

    return np.linalg.solve(A.T, b)


def centered_fd(dx=None, n=None, order=1, x=None):
    # x = list of points to be used in the derivative approximation (LENGTH MUST BE ODD)
    # dx = interval spacing
    # n = number of points used in approximation (MUST BE ODD)

    if x != None:
        n = len(x)
        delta_x = np.array(x) - x[n//2]
    elif dx != None and n!=None:
        delta_x = np.linspace(-n*dx//2, n*dx//2, dx, endpoint=True)
    else:
        raise Exception('specify x or dx and n')
    
    if n%2 == 0:
        raise Exception('Need to use an odd number of points')
    
    A = np.vander(delta_x, increasing=True)
    f = np.array([factorial(i) for i in range(n)])
    A = A/f
    b = np.zeros(n)
    b[order] = 1

    return np.linalg.solve(A.T, b)


# generalized claculator

def general_fd(x, index=0, order=1):
    # x = list of points ot be used in derivative approximation
    # index = point where the derivative is to be approximated
    # order = what order of derivative to compute

    n = len(x)
    delta_x = np.array(x) - x[index]

    A = np.vander(delta_x, increasing=True)
    f = np.array([factorial(i) for i in range(n)])
    A = A/f
    b = np.zeros(n)
    b[order] = 1
    return np.linalg.solve(A.T, b)


print()