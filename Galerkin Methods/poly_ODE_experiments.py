from Galerkin_poly_ODE import solve
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as p
from numpy.random import randint
import numpy as np


def generate_poly(n=5):
    
    while True:
        roots = randint(-5, 10, n-1) / 5

        # force origin to be a root
        f = [0, 1]

        for i in range(n-1):
            f = p.polymul(f, [roots[i], -1])

        # normalize to force f(1) = 1
        if sum(f) != 0:
            f = f/sum(f)
            break

    return f


n = 6
for i in range(10):
    f = generate_poly(n)
    t = np.linspace(-0.1, 1.1, 100)
    y = p.polyval(t, f)

    plt.plot(t, y, label='original')

    ddf = p.polyder(p.polyder(f))
    solution_approximations = {}
    for i in range(2, n+1):
        v = solve(ddf, i)
        plt.plot(t, p.polyval(t, v), label=f'{str(i-1)}th order approx')

    plt.legend()
    plt.show()