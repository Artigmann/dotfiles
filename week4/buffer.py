import cPickle as pickle
import os

# TODO: Buffer needs timestamps.
class Buffer:
    def __init__(self, func):
        self.func = func
        self.filename = func.__name__ + ".buf"

        self.buffer = {}
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as f:
                try:
                    self.buffer = pickle.load(f)
                except EOFError:
                    self.buffer = {}

    def __del__(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.buffer, f)

    def __call__(self, arg):
        if arg in self.buffer:
            return self.buffer[arg]
        retval = self.func(arg)
        self.buffer[arg] = retval
        return retval
