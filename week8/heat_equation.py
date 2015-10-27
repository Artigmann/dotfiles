#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt


def heat_equation(t0, t1, dt, n, m, u, f, nu, verbose=False):
    """
    Solves heat equation where t0 is start time, t1 is end time,
    dt is time step, n is rectangle is rectangle width, m is rectangle height,
    u are the initial values (as a n x m list), f is the heat source function
    (also a n x m list) and nu is thermal diffusivity. Returns the result as a
    n x m list.

    Note that this function is destructive and will manipulate the given u
    argument.
    """
    if verbose:
        print "Solving with python heat equation solver."
    t = t0
    while t < t1:
        # Init u_n to zero.
        u_n = [([0] * n) for _ in xrange(m)]
        # u_n = [[0] * n] * m
        for i in xrange(1, m-1):
            for j in xrange(1, n-1):
                u_n[i][j] = u[i][j] \
                            + dt*(nu*u[i-1][j] + nu*u[i][j-1] -
                                  4*nu*u[i][j] + nu*u[i][j+1] +
                                  nu*u[i+1][j] + f[i][j])
        u = u_n
        t += dt
    return u


def heat_equation_plot(t0, t1, dt, n, m, u, f, nu, solver_func=heat_equation,
                       verbose=False, save_to=None, time=False):
    """
    Solves and plots heat equation where t0 is start time, t1 is end time,
    dt is time step, n is rectangle is rectangle width, m is rectangle height,
    u are the initial values (as a n x m list), f is the heat source function
    (also a n x m list), nu is thermal diffusivity, solver_func is the
    solver function you want to use, verbose gives verbose output,
    save_to is a file handle to save the file to. Returns the solved
    heat_equation.

    Note that this function is destructive and will manipulate the given u
    argument.
    """
    if verbose:
        print "Entering plotting function"
    # Init subplots and create t0 plot.
    fig, axes = plt.subplots(nrows=1, ncols=2)
    axes[0].imshow(u, plt.get_cmap("gray"))

    # Call the given solver function, this lets us plot with other solvers.
    u = solver_func(t0, t1, dt, n, m, u, f, nu, verbose)

    # Plot t1 plot and colorbar.
    im = axes[1].imshow(u, plt.get_cmap("gray"))
    plt.colorbar(im, ax=axes.ravel().tolist())

    if save_to:
        if verbose:
            print "Saving figure to {}".format(save_to.name)
        plt.savefig(save_to)

    plt.show()

    # Return u so UI can save.
    return u

if __name__ == '__main__':
    # Set initial values for a run if we call the file.
    t0 = 0
    t1 = 1000
    dt = 0.1
    n = 50
    m = 100
    u = [([0] * n) for y in xrange(m)]
    f = [([1] * n) for y in xrange(m)]
    nu = 1.
    heat_equation_plot(t0, t1, dt, n, m, u, f, nu)
