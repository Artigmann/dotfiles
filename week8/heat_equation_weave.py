#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from scipy import weave
from heat_equation import heat_equation_plot


def heat_equation_weave(t0, t1, dt, n, m, u, f, nu):
    """
    Solves heat equation where t0 is start time, t1 is end time,
    dt is time step, n is rectangle is rectangle width, m is rectangle height,
    u are the initial values (as a n x m numpy array), f is the heat source
    function (also a n x m numpy array) and nu is thermal diffusivity. Returns
    the result as a n x m numpy array.

    Note that this function is destructive and will manipulate the given u
    argument.
    """
    # Do some type conversions to ensure the C code will run nicely.
    t0 = float(t0)
    t1 = float(t1)
    dt = float(dt)
    nu = float(nu)

    # Do some extra instance checking as weave errors can be hard to decipher.
    assert(isinstance(m, int))
    assert(isinstance(n, int))
    assert(isinstance(u, np.ndarray))
    assert(isinstance(f, np.ndarray))

    # Copy array so we can pointer swap.
    u_2 = np.copy(u)

    # C-ish code to solve the equation uses pointer swapping to avoid copying
    # the array.
    code = r"""
    bool is_u = false; /* Keeps track of currently active u. */
    int i, j;
    for (/*t0*/; t0 < t1; t0 += dt) {
        /* Time step loop */
        for (i = 1; i < Nu[0] - 1; i++) {
            for (j = 1; j < Nu[1] - 1; j++) {
                u[i*Nu[1] + j] = u_2[i*Nu[1] + j] +
                                 dt*(nu*u_2[(i-1)*Nu[1] + j] +
                                     nu*u_2[i*Nu[1] + j-1] -
                                     4*nu*u_2[i*Nu[1] + j] +
                                     nu*u_2[i*Nu[1] + j+1] +
                                     nu*u_2[(i+1)*Nu[1] + j] +
                                     F2(i, j));
            }
        }

        /* Pointer swap, to avoid copying data for every iteration. */
        double *tmp = u;
        u = u_2;
        u_2 = tmp;

        /* Which is currently active of u and u_2? */
        if (is_u) {
            is_u = false;
        } else {
            is_u = true;
        }
    }

    /* Return boolean to tell current u. */
    return_val = is_u;
    """

    # Exectute weave code.
    is_u = weave.inline(code, ["t0", "t1", "dt", "nu", "u", "f", "u_2"])

    # Return the correct array.
    if is_u:
        return u
    else:
        return u_2


if __name__ == '__main__':
    # Set initial values for a run if we call the file.
    t0 = 0.
    t1 = 1000.
    dt = 0.1
    n = 50
    m = 100
    u = np.zeros((m, n))
    f = np.ones((m, n))
    nu = 1.
    heat_equation_plot(t0, t1, dt, n, m, u, f, nu, heat_equation_weave)
