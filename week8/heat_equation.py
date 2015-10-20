#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

def heat_equation(t0, t1, dt, n, m, u, f, nu):
    t = t0
    while t < t1:
        u_n = [[0 for x in xrange(n)] for y in xrange(m)]
        for i in xrange(1, m-1):
            for j in xrange(1, n-1):
                u_n[i][j] = u[i][j] \
                            + dt*(nu*u[i-1][j] + nu*u[i][j-1] - 4*nu*u[i][j] +
                                  nu*u[i][j+1] + nu*u[i+1][j] + f[i][j])
        u = u_n
        t += dt

    plt.imshow(u, plt.get_cmap("gray_r"))
    plt.show()

if __name__ == '__main__':
    n = 50
    m = 100
    u = [([0] * n) for y in xrange(m)]
    f = [([1] * n) for y in xrange(m)]
    heat_equation(0, 1000, 0.1, n, m, u, f, 1)

    raw_input("Press Return key to quit:")
