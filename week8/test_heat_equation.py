#!/usr/bin/env python
# -*- coding: utf-8 -*-

import heat_equation_weave as hew
import numpy as np
from math import sin, pi


def test_heat_equation_weave_err():
    """
    Tests if the error of the heat equation solver is within the range given by
    the assignment.
    """
    t0 = 0
    t1 = 1000
    dt = 0.1
    n = 50
    m = 100
    nu = 1.
    u = np.zeros((m, n))

    # Set f, according to the formula.
    f = np.empty((m, n))
    for i in xrange(n):
        for j in xrange(m):
            f[j, i] = nu*((2*pi/(m-1))**2 + (2*pi/(n-1))**2) \
                      * sin(2*pi/(n-1)*i)*sin(2*pi/(m-1)*j)

    # Set analytic_u, according to the formula.
    analytic_u = np.empty((m, n))
    for i in xrange(n):
        for j in xrange(m):
            analytic_u[j, i] = sin(2*pi/(n-1)*i)*sin(2*pi/(m-1)*j)

    u_solved = hew.heat_equation_weave(t0, t1, dt, n, m, np.copy(u), f, nu)

    err_1 = (abs(u_solved - analytic_u)).max()

    assert(err_1 < 0.0012)


def test_heat_equation_weave_decrease():
    """
    Tests if the error of the heat equation solver decreases as we increase
    the size of the rectangle. To get this to work properly I had to increase
    the end-time, as suggested by Simon Funke on Piazza.
    """
    # Common initial values.
    t0 = 0
    t1 = 2000
    dt = 0.1
    nu = 1.

    # Get first error.
    n = 50
    m = 100
    u = np.zeros((m, n))
    # Set f, according to formula.
    f = np.empty((m, n))
    for i in xrange(n):
        for j in xrange(m):
            f[j, i] = nu*((2*pi/(m-1))**2 + (2*pi/(n-1))**2) \
                      * sin(2*pi/(n-1)*i)*sin(2*pi/(m-1)*j)

    # Set analytic_u, according to formula
    analytic_u = np.empty((m, n))
    for i in xrange(n):
        for j in xrange(m):
            analytic_u[j, i] = sin(2*pi/(n-1)*i)*sin(2*pi/(m-1)*j)

    u_solved = hew.heat_equation_weave(t0, t1, dt, n, m, np.copy(u), f, nu)
    err_1 = (abs(u_solved - analytic_u)).max()

    # Get second error.
    n = 100
    m = 200
    u = np.zeros((m, n))
    # Set f according to formula.
    f = np.empty((m, n))
    for i in xrange(n):
        for j in xrange(m):
            f[j, i] = nu*((2*pi/(m-1))**2 + (2*pi/(n-1))**2) \
                      * sin(2*pi/(n-1)*i)*sin(2*pi/(m-1)*j)

    # Set analytic_u according to formula.
    analytic_u = np.empty((m, n))
    for i in xrange(n):
        for j in xrange(m):
            analytic_u[j, i] = sin(2*pi/(n-1)*i)*sin(2*pi/(m-1)*j)

    u_solved = hew.heat_equation_weave(t0, t1, dt, n, m, np.copy(u), f, nu)

    err_2 = (abs(u_solved - analytic_u)).max()

    # Assert that err_2 is smaller than err_1.
    assert(err_1 > err_2)
