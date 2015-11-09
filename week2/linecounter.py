#!/usr/bin/env python
"""
Prints number of lines in given files.
"""

import sys

if len(sys.argv) < 2:
    # No filenames given, print usage info.
    print "USAGE: python {0} FILE1 [FILE2] ...".format(sys.argv[0])
    print "Prints the number of lines per file given."
    sys.exit()

for filename in sys.argv[1:]:
    try:
        file = open(filename, "r")
    except IOError:
        # No file? Print error and continue with the other files.
        sys.stderr.write("Could not open {0}!\n".format(filename))
        continue

    # Iterate through lines and increment counter
    lines = 0
    for _ in file:
        lines += 1
    print "{0}: {1}".format(filename, lines)
    file.close()
