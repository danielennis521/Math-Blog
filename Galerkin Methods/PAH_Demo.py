from Physics_Aware_Heat_LSTQ import solve
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(precision=3, suppress=True)


def true_heat(x, t):
    return np.sin(4*np.pi*x)*np.exp(-(4*np.pi)**2 * t)


n = 7
nx = 9
nt = 200
dt = 1e-4
x = np.linspace(0, 1, nx, endpoint=True)
y = [true_heat(x, dt*t) for t in range(nt)]


loci = np.linspace(x[0], x[-1], 50, endpoint=True)
u = solve(x, y, dt, n)
for i in range(len(u)):
    plt.ylim([-1, 1])
    plt.plot(loci, u[i])
    plt.plot(x, y[i], linestyle='--')
    plt.pause(0.1)
    plt.cla()
