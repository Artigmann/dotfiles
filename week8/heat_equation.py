#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt


def heat_equation_plot(t0, t1, dt, n, m, u, f, nu):
    """
    Solves and plots heat equation where t0 is start time, t1 is end time,
    dt is time step, n is rectangle is rectangle width, m is rectangle height,
    u are the initial values (as a n x m list), f is the heat source function
    (also a n x m list) and nu is thermal diffusivity.
    """

    # Init subplots and create t0 plot.
    fig, axes = plt.subplots(nrows=1, ncols=2)
    axes[0].imshow(u, plt.get_cmap("gray"))

    t = t0
    while t < t1:
        # Init u_n to zero.
        u_n = [([0] * n) for y in xrange(m)]
        for i in xrange(1, m-1):
            for j in xrange(1, n-1):
                u_n[i][j] = u[i][j] \
                            + dt*(nu*u[i-1][j] + nu*u[i][j-1] - 4*nu*u[i][j] +
                                  nu*u[i][j+1] + nu*u[i+1][j] + f[i][j])
        u = u_n
        t += dt

    # Plot t1 plot and colorbar.
    im = axes[1].imshow(u, plt.get_cmap("gray"))
    plt.colorbar(im, ax=axes.ravel().tolist())
    plt.show()

if __name__ == '__main__':
    # Set initial values.
    t0 = 0
    t1 = 1000
    dt = 0.1
    n = 50
    m = 100
    u = [([0] * n) for y in xrange(m)]
    f = [([1] * n) for y in xrange(m)]
    nu = 1.
    heat_equation_plot(t0, t1, dt, n, m, u, f, nu)
