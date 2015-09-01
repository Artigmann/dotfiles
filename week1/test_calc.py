import os
from subprocess import Popen, PIPE

def calc(expr):
    """ Calls the calculator on the input and returns the result. """

    process = Popen(["bash", "calc.sh", expr], stdout=PIPE)
    (stdout, stderr) = process.communicate()
    exit_code = process.wait()
    assert exit_code == 0

    print stdout

    # Extract solution
    solution = stdout.split("=")[-1].strip()

    return solution


def test_calc():
    assert float(calc("1+2"))  == 3
    assert float(calc("3-2"))  == 1
    assert float(calc("30-55"))  == -25
    assert float(calc("2*(-55)"))  == -110
    assert float(calc("2*5"))  == 10
    assert float(calc("10/2"))  == 5
