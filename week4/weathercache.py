import cPickle as pickle
import os
import errno
import string
from datetime import datetime, timedelta

CACHE_PATH = "weathercache/"

class WeatherCache:
    def __init__(self, func, timestamp=None):
        self.func = func
        self.timestamp = timestamp # TODO: Rename.

        if not os.path.exists(CACHE_PATH):
            os.mkdir(CACHE_PATH)

        if not os.path.isdir(CACHE_PATH):
            raise EnvironmentError(errno.ENOTDIR, CACHE_PATH + " is not a directory!")

    def __call__(self, arg):
        if self.timestamp is not None:
            cur_time = self.timestamp
        else:
            cur_time = datetime.now()

        filename = CACHE_PATH + "".join([c for c in arg if c.isalpha() or c.isdigit()]).rstrip() + ".tmp"

        if os.path.exists(filename):
            print "File: " + filename + " exists!"
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
                    print "Cache: Returning from file"
                    return pickle.load(f)

        retval = self.func(arg)
        with open(filename, "wb") as f:
            pickle.dump(retval, f)
        print "Cache: Returning from function"
        return retval
