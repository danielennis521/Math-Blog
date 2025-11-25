import numpy as np
from math import factorial



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


def approx_deriv(x, y, window, order=1):
    # x = list of points ot be used in derivative approximation
    # y = list of function values associated with the points x
    # window = number of points used to approximate the derivative
    # order = what order of derivative to compute

    dy = np.zeros(len(x))

    for i in range(len(x)):
        if window//2 > i:
            x_window = x[:window]
            y_window = y[:window]
            c = general_fd(x_window, index=i, order=order)
            dy[i] = c.dot(y_window)
        elif len(x) - window//2 - 1 < i:
            x_window = x[-window:]
            y_window = y[-window:]
            c = general_fd(x_window, index=i+window-len(x), order=order)
            dy[i] = c.dot(y_window)
        else:
            x_window = x[i-window//2: i+window//2+1]
            y_window = y[i-window//2: i+window//2+1]
            c = general_fd(x_window, index=window//2, order=order)
            dy[i] = c.dot(y_window)

    return dy


def generate_difference_schemes(x, window, order=1):
    # x = list of points ot be used in derivative approximation
    # y = list of function values associated with the points x
    # window = number of points used to approximate the derivative
    # order = what order of derivative to compute

    n = len(x)
    schemes = []

    for i in range(n):
        if window//2 > i:
            x_window = x[:window]
            c = general_fd(x_window, index=i, order=order)
            index = [range(window)]
        elif n - window//2 - 1 < i:
            x_window = x[-window:]
            c = general_fd(x_window, index=i+window-n, order=order)
            index = [range(n-window, n)]
        else:
            x_window = x[i-window//2: i+window//2+1]
            c = general_fd(x_window, index=window//2, order=order)
            index = [range(i-window//2, i+window//2+1)]
        schemes.append((index, c))

    return schemes



