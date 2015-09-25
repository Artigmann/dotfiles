import cPickle as pickle
import os
from datetime import datetime, timedelta

# TODO: Buffer needs timestamps. Will need to take care of periods ...
class LazyBuf:
    def __init__(self, func, filename, timestamp = None):
        self.func = func
        self.filename = filename
        self.timestamp = timestamp # TODO: Rename.

        self.buf = {}
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as f:
                try:
                    self.buf = pickle.load(f)
                except EOFError:
                    self.buf = {}

    def __del__(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.buf, f)

    def __call__(self, arg):
        if self.timestamp is not None:
            cur_time = timestamp
        else:
            cur_time = datetime.now()

        if arg in self.buf and cur_time < self.buf[arg][0]:
            print "Getting from buffer"
            return self.buf[arg][1]

        print "Getting from function"
        if cur_time.hour < 6:
            valid_to = cur_time.replace(hour=6, minute=0, second=0)
        elif cur_time.hour < 12:
            valid_to = cur_time.replace(hour=12, minute=0, second=0)
        elif cur_time.hour < 18:
            valid_to = cur_time.replace(hour=18, minute=0, second=0)
        else:
            valid_to = cur_time.replace(hour=0, minute=0, second=0) + timedelta(days=1)
        retval = self.func(arg)
        self.buf[arg] = (valid_to, retval)
        return retval
