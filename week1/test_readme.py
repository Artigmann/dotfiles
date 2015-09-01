import os.path

files = ["Readme.txt", "readme.txt"]
for fn in files:
    if os.path.isfile(fn):
        break

assert os.path.isfile(fn)

f = open(fn, "r")
assert "Hello world" in " ".join(f.readlines())
