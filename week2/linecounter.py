#!/usr/bin/env python

import sys

for filename in sys.argv[1:]:
    try:
        file = open(filename, "r")
    except IOError:
        print "Could not open {0}!".format(filename)
        continue

    # Iterate through lines and increment counter
    lines = 0
    while file.readline():
        lines += 1
    print "{0}: {1}".format(filename, lines)
    file.close()
