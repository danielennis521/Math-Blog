# The code here solves the simple second order ODE with with polynomial forcing, that is
#                       u''(t) = sum(c_i * t^i) with u(0)=0 and u(1)=1
# the solution is done by finding a polynomial of a specified order that "nearly solves"
# the ODE in the least sqaures sense.

import numpy as np
import numpy.linalg as la



def design_matrix(n):
    A = np.zeros([n, n])

    # second derivative approximations 
    for i in range(2, n):
        for j in range(2, n):
            A[i][j] = j*(j-1)/(j+i-3)
    
    # boundary conditions
    A[0][0] = 1
    for j in range(n):
        A[1][j] = 1

    return A



def forcing_vector(f, n):
    b = np.zeros(n)
    m = len(f)

    for i in range(2, n):
        for j in range(m):
            b[i] += f[j]/(j+i-1)

    # boundary condition
    b[1] = 1 

    return b



def solve(f, n):
    # inputs
    # f: the coefficients of the forcing polynomial starting with the constant term
    # n: the order of the polynomial used for the approximate solution

    A = design_matrix(n)
    b = forcing_vector(f, n)

    return la.solve(A, b)
