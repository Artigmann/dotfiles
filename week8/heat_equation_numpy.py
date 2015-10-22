#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np


def heat_equation_np(t0, t1, dt, n, m, u, f, nu):
    """
    Solves heat equation where t0 is start time, t1 is end time,
    dt is time step, n is rectangle is rectangle width, m is rectangle height,
    u are the initial values (as a n x m list), f is the heat source function
    (also a n x m list) and nu is thermal diffusivity. Returns the result as a
    n x m list.
    """
    t = t0
    while t < t1:
        u[1:-1, 1:-1] += dt*(nu*u[:-2, 1:-1] + nu*u[1:-1, :-2] -
                             4*nu*u[1:-1, 1:-1] + nu*u[1:-1, 2:] +
                             nu*u[2:, 1:-1] + f[1:-1, 1:-1])
        t += dt
    return u


def heat_equation_plot_np(t0, t1, dt, n, m, u, f, nu):
    """
    Solves and plots heat equation where t0 is start time, t1 is end time,
    dt is time step, n is rectangle is rectangle width, m is rectangle height,
    u are the initial values (as a n x m list), f is the heat source function
    (also a n x m list) and nu is thermal diffusivity.
    """
    # Init subplots and create t0 plot.
    fig, axes = plt.subplots(nrows=1, ncols=2)
    axes[0].imshow(u, plt.get_cmap("gray"))

    u = heat_equation_np(t0, t1, dt, n, m, u, f, nu)

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
    u = np.zeros((m, n))
    f = np.empty((m, n))
    f.fill(1)
    nu = 1.
    heat_equation_plot_np(t0, t1, dt, n, m, u, f, nu)
