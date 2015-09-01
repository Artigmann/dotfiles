import os
import signal
from subprocess import Popen, PIPE
from time import sleep

def test_clock():
    process = Popen(["bash", "clock.sh"], stdout=PIPE, shell=False)

    sleep(2)
    process.send_signal(signal.SIGINT)   # send Ctrl-C signal

    (stdout, stderr) = process.communicate()

    stdout.lower().endswith("bye bye")
