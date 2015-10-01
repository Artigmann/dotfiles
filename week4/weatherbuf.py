#!/usr/bin/env python
# encoding: utf-8
import cPickle as pickle
import os
import errno
import string
from datetime import datetime, timedelta

CACHE_PATH = "weatherbuf/"

class WeatherBuf:
    """
    A buffer to save files if they fulfill certain specific age requirements.
    It takes a timestamp argument to facilitate testing of the buffers
    functionality. If timestamp is current system time will be replaced with
    the timestamp for all operations pertaining to the buffer.

    The buffer saves all buffer files in the directory given by CACHE_PATH.

    Usage:
    func = WeatherBuf(old_func)
    func(arg)
    """
    def __init__(self, func, timestamp=None):
        self.func = func
        self.timestamp = timestamp

        if not os.path.exists(CACHE_PATH):
            os.mkdir(CACHE_PATH)

        if not os.path.isdir(CACHE_PATH):
            raise EnvironmentError(errno.ENOTDIR, CACHE_PATH + " is not a directory!")

    def __call__(self, arg):
        # If timestamp is set we use it, if not we use current system time.
        if self.timestamp:
            cur_time = datetime.fromtimestamp(self.timestamp)
        else:
            cur_time = datetime.now()

        filename = CACHE_PATH + "".join([c for c in arg if c.isalpha() or c.isdigit()]).rstrip() + ".tmp"

        if os.path.exists(filename):
            # File exists, check if it matches the time requirements.
            file_time = datetime.fromtimestamp(os.path.getmtime(filename))
            if file_time.hour < 6:
                valid_to = file_time.replace(hour=6, minute=0, second=0)
            elif file_time.hour < 12:
                valid_to = file_time.replace(hour=12, minute=0, second=0)
            elif file_time.hour < 18:
                valid_to = file_time.replace(hour=18, minute=0, second=0)
            else:
                valid_to = file_time.replace(hour=0, minute=0, second=0) + timedelta(days=1)

            if cur_time < valid_to:
                with open(filename, "rb") as f:
                    return pickle.load(f)

        retval = self.func(arg)
        with open(filename, "wb") as f:
            pickle.dump(retval, f)
        if self.timestamp:
            # If timestamp is set we will modify the mtime.
            os.utime(filename, (self.timestamp, self.timestamp))
        return retval
