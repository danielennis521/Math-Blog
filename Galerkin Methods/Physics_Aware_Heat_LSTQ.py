# Given a set of temperature measurements over time we can compute an
# approximation of the full temperature distribution. Since du/dt = d^2u/dx^2
# the time rate of change gives us an estimate of the curvature at that point. 

import numpy as np
import numpy.linalg as la
import numpy.polynomial.polynomial as p


def heat_matrix(x, n):
    B = np.zeros([len(x), n])
    A = np.vander(x, n-2, increasing=True)
    for i in range(n-2):
        A[:, i] *= (i+1)*(i+2)
    
    B[0:, 2:] = A
    B[0, 0] = 1
    B[0, 1:] = 0
    B[-1, :] = 1
    return B


def lstq_matrix(x, n):
    return np.vander(x, n, increasing=True)


def heat_forcing(y0, y1, dt):
    return (y1 - y0)/dt


def lstq_forcing(y):
    return y


def solve(x, y, dt, n):
    # imputs
    # x: list of points on the interval [0, 1] where measurements were taken (x must include 0 and 1)
    # y: 2d array where y[i][j] is the measured temp at time j and point x[i]
    # dt: length of time between measurements
    # n: order of the polynomial approximation to be used (1=linear, 2=quadratic, etc)

    u = []
    nt = len(y)
    loci = np.linspace(x[0], x[-1], 50, endpoint=True)
    #A = heat_matrix(x, n+1)
    B = lstq_matrix(x, n+1)

    for i in range(nt-1):
        #c = heat_forcing(y[i], y[i+1], dt)
        d = lstq_forcing(y[i])

        coeff = la.lstsq(B, d)[0]
        u.append(p.polyval(loci, coeff))

    return u
