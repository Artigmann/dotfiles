# This script can be used to automatically check the assignments of students
import py
import os
import sys
import argparse
verbose = True

# List of assignment names and achievable points
test_list = [("readme",   2),
             ("calc",     2),
             ("compress", 4),
             ("clock",    2),
            ]
max_points = sum([x[1] for x in test_list])


def run_test(name):
    test_name = "test_" + name
    if not os.path.isfile(test_name + ".py"):
        print "Test file '{}' does not exist.".format(test_name + ".py")
        exit(1)
    if verbose:
        return py.test.cmdline.main(["-s", "-k", test_name])
    else:
        return py.test.cmdline.main(["-q", "-k", test_name])

def run_all_tests():
    summary = ""
    point_list = []

    for test, points in test_list:
        exit_code = run_test(test)
        if exit_code == 0:
            summary += "Test {} passed ({} points)\n".format(test, points)
            point_list.append(points)
        else:
            summary += "Test {} failed (0 points)\n".format(test)

    total_points = sum(point_list)
    summary += "Rough (!!) estimate of points: {} / {}".format(total_points, max_points)
    return summary, point_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tests assignemnts.')
    parser.add_argument('-s', '--silent', action='store_false',
                        help='Surpress most output')
    args = parser.parse_args()
    verbose = args.silent

    print run_all_tests()[0]
