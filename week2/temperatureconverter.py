#!/usr/bin/env python
"""
Prints temperature given in fahrenheit as celsius.
"""

import sys

if len(sys.argv) < 2:
    print "USAGE: python {0} FAHRENHEIT".format(sys.argv[0])
    print "Converts temperature in fahrenheit to temperature in celsius."
    sys.exit()

fahrenheit = float(sys.argv[1])

celsius = (fahrenheit - 32) * 5/9.
print "{0:.1f} fahrenheit is {1:.1f} celsius.".format(fahrenheit, celsius)
