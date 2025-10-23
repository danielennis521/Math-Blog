from Physics_Aware_Heat_LSTQ import heat_matrix, heat_forcing, lstq_forcing, lstq_matrix
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as la
import numpy.polynomial.polynomial as p
np.set_printoptions(precision=3, suppress=True)


def true_heat(x, t):
    return np.sin(np.pi*x)*np.exp(-np.pi**2 * t)


n = 7
nx = 30
dt = 0.01
x = np.linspace(0, 1, nx, endpoint=True)
y0 = true_heat(x, 0) + np.random.normal(0.0, 0.01, nx)
y1 = true_heat(x, dt) + np.random.normal(0.0, 0.01, nx)

A = lstq_matrix(x, n)
c = la.lstsq(A, y0)[0]
B = heat_matrix(x, n)
d = heat_forcing(y0, y1, dt)

d[0] = 0
d[-1] = 0
B[0, 0] = 1
B[0, 1:] = 0
B[-1, :] = 1
ch = la.lstsq(B, d)[0]

print(c)
print(ch)
plt.plot(x, p.polyval(x, c), color='b')
plt.plot(np.linspace(0, 1, 100, endpoint=True), 
         true_heat(np.linspace(0, 1, 100, endpoint=True), 0),
         color='r')
plt.plot(x, p.polyval(x, ch), color='g')
plt.show()