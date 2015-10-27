#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basic UI written as a straightforward script using argparse. Uses cPickle to
load and unload potential files. Uses the written heat_equation* files to
solve the heat equation.
"""

import argparse
import cPickle as pickle
import numpy as np
import heat_equation as he
import heat_equation_numpy as hen
import heat_equation_weave as hew

parser = argparse.ArgumentParser(description="Solve given heat equation, "
                                 "required arguments are dimensions or input "
                                 "file and end time.")

# Running options.
group_run = parser.add_argument_group("Running options")
group_run.add_argument("-v", "--verbose", action="store_true",
                       help="Print extra run-time information.")
group_run.add_argument("-t", "--time", action="store_true",
                       help="Time the running of the of the solver.")
group_run.add_argument("-i", "--solver-implementation", dest="solver",
                       default="weave",
                       choices=["python", "numpy", "weave"],
                       help="What solver to use, valid choices are python, "
                       "numpy and weave.")

# Parameters to equation
group_param = parser.add_argument_group("Equation parameters")
group_param.add_argument("-dt", "--time-step", type=float, dest="dt",
                         default=0.1,
                         help="Timestep, default value is 0.1.")
group_param.add_argument("-nu", "--thermal-diffusivity", type=float,
                         dest="nu", default=1.0,
                         help="Thermal diffusivity, default value is 1.0")
group_param.add_argument("-f", "--constant-heat", type=float, default=1.0,
                         dest="f",
                         help="Constant heat source, default value is 1.0")
group_param.add_argument("-t0", "--start-time", type=float, default=0.0,
                         dest="t0",
                         help="Time at beginning of equation, default value "
                         "is 0.")
group_param.add_argument("-t1", "--end-time", type=float, default=1000.0,
                         dest="t1",
                         help="Time to end equation, default value is 1000.0.")

# Input/output
group_inout = parser.add_argument_group("Input/output")
group_inout.add_argument("-s", "--save_plot", type=argparse.FileType("w"),
                         help="Save plot with given name")
group_inout.add_argument("-of", "--output-file", type=argparse.FileType("w"),
                         help="Name of eventual output file.")
group_in = group_inout.add_mutually_exclusive_group(required=True)
group_in.add_argument("-if", "--input-file", type=argparse.FileType("r"),
                      help="Start with u from given file.")
group_in.add_argument("-d", "--dimensions", metavar=("N", "M"), type=int,
                      nargs=2, help="Start with u at 0 with dimensions given "
                                    "by -d N M.")

args = parser.parse_args()


# Set verbose flag
verbose = args.verbose

# Handle creation of u, set n and m.
if args.input_file:
    # Load potential input file.
    if verbose:
        print "Getting u from file."
    u = pickle.load(args.input_file)
    if not isinstance(u, np.ndarray):
        raise ValueError("Given input file did not contain numpy "
                         "array.")
    m = len(u)
    n = len(u[0])
else:
    # Create u based on given dimensions.
    n = args.dimensions[0]
    m = args.dimensions[1]
    if args.verbose:
        print "Creating u with dimensions {}x{}".format(n, m)
    u = np.zeros((m, n))

# Get solver.
if args.solver == "python":
    solver = he.heat_equation
elif args.solver == "numpy":
    solver = hen.heat_equation_numpy
elif args.solver == "weave":
    solver = hew.heat_equation_weave


# Create f.
f = np.zeros((m, n)) + args.f


if args.time:
    # Time stuff, we only import the timeit module here if we actually need it.
    from timeit import Timer
    if verbose:
        print "Will now time the solver 3 times, this could take a while in " \
              "some cases."
    t = Timer(lambda: solver(args.t0, args.t1, args.dt, n, m, np.copy(u), f,
                             args.nu, verbose=verbose))
    times = t.repeat(repeat=3, number=1)
    if verbose:
        print "All run times:"
        print times
    print "Best running time in 3 runs were {} seconds.".format(min(times))


# Plot, magic happens here.
u = he.heat_equation_plot(args.t0, args.t1, args.dt, n, m, u, f, args.nu,
                          solver, verbose, args.save_plot)


# Handle potential output file.
if args.output_file:
    if not isinstance(u, np.ndarray):
        # Convert potential list to numpy array.
        if verbose:
            print "Converting list to numpy array"
        u = np.array(u)

    if verbose:
        print "Writing array to file {}".format(args.output_file.name)
    pickle.dump(u, args.output_file)
