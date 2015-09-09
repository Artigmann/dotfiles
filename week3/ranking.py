#!/usr/bin/env python
"""
When run, gets data from the file data.log and parses it to get min, max and
average CPU time values.
"""

import sys
from collections import defaultdict


def get_data(filename):
    """
    Gets data from a file formatted with the data.log formatting from
    assignment 3.4.
    """
    f = open(filename, 'r')
    dic = defaultdict(list)
    for line in f:
        if "CPU" in line:
            words = line.split()
            if len(words) < 4:
                sys.stderr.write("Error encountered in file, aborting.\n")
                break
            name = words[1]
            time = float(words[3])
            dic[name].append(time)
    f.close()

    return dic

if __name__ == '__main__':
    data = get_data("data.log")
    for key in data:
        test = data[key]
        print "\nTest name: {}".format(key)
        print "CPU time:  {:.1f} s (min)".format(min(test))
        print "CPU time:  {:.1f} s (avg)".format(sum(test) / len(test))
        print "CPU time:  {:.1f} s (max)".format(max(test))
