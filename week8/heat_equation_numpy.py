#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from heat_equation import heat_equation_plot


def heat_equation_numpy(t0, t1, dt, n, m, u, f, nu, verbose=False):
    """
    Solves heat equation where t0 is start time, t1 is end time,
    dt is time step, n is rectangle is rectangle width, m is rectangle height,
    u are the initial values (as a n x m numpy array), f is the heat source
    function (also a n x m numpy array) and nu is thermal diffusivity. Returns
    the result as a n x m numpy array.

    Note that this function is destructive and will manipulate the given u
    argument.
    """
    if verbose:
        print "Solving with numpy heat equation solver."
    t = t0
    while t < t1:
        u[1:-1, 1:-1] += dt*(nu*u[:-2, 1:-1] + nu*u[1:-1, :-2] -
                             4*nu*u[1:-1, 1:-1] + nu*u[1:-1, 2:] +
                             nu*u[2:, 1:-1] + f[1:-1, 1:-1])
        t += dt
    return u


if __name__ == '__main__':
    # Set initial values for a run if we call the file.
    t0 = 0
    t1 = 1000
    dt = 0.1
    n = 50
    m = 100
    u = np.zeros((m, n))
    f = np.empty((m, n))
    f.fill(1)
    nu = 1.
    heat_equation_plot(t0, t1, dt, n, m, u, f, nu, heat_equation_numpy)
