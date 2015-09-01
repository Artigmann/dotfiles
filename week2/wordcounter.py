#!/usr/bin/env python
"""
Prints word counts for given files.
"""

import sys

if len(sys.argv) < 2:
    # No filenames given, print usage info.
    print "USAGE: python {0} FILE1 [FILE2] ...".format(sys.argv[0])
    print "Prints the number of words per file given."
    sys.exit()

for filename in sys.argv[1:]:
    try:
        file = open(filename, "r")
    except IOError:
        # On IOError we print a message and continue with the other files.
        sys.stderr.write("Could not open {0}!\n".format(filename))
        continue

    # Iterate through lines and increment counter per word
    wordcount = 0
    while True:
        line = file.readline()
        if not line:
            # Empty line means eof, break loop.
            break
        words = line.split()
        for _ in words:
            wordcount += 1
    print "{0}: {1}".format(filename, wordcount)
    file.close()
