import os
import shutil
from subprocess import Popen, PIPE

def create_file(filename, size_kb):
    """ Creates a new file of the specified size """
    with open(filename, "wb") as out:
        out.seek((1024 * size_kb) - 1)
        out.write('\0')


def compress(basedir, filesize):
    """ Calls the compresses script. """

    process = Popen(["bash", "compress.sh", basedir, filesize])
    exit_code = process.wait()
    assert exit_code == 0


def decompress(basedir):
    """ Calls the compresses script. """

    process = Popen(["bash", "decompress.sh", basedir])
    exit_code = process.wait()
    assert exit_code == 0

def test_compress_and_decompress():
    basedir = "compress_tmp"

    # Clean up in case we failed in previous run
    shutil.rmtree(basedir, ignore_errors=True)

    # Create directory tree
    os.makedirs(basedir)
    os.makedirs(os.path.join(basedir, "subdir"))

    # Create some files
    file0 = "file0.txt"  # Note: not in basedir
    file1 = os.path.join(basedir, "file1.txt")
    file2 = os.path.join(basedir, "subdir", "file2.txt")
    file3 = os.path.join(basedir, "subdir", "file3.txt")

    create_file(file0, 120)
    create_file(file1, 80)
    create_file(file2, 50)
    create_file(file3, 100)

    # Run the compression script
    compress(basedir, "60")

    assert os.path.isfile(file0)  # Should not have been compressed
    assert os.path.isfile(file1 + ".gz")  # Should have been compressed
    assert os.path.isfile(file2)  # Should not have been compressed
    assert os.path.isfile(file3 + ".gz")  # Should have beend compressed

    assert os.stat(file0).st_size > 119*1024
    assert os.stat(file1 + ".gz").st_size < 1024
    assert os.stat(file2).st_size > 1024*49
    assert os.stat(file3 + ".gz").st_size < 1024

    # Run the decompression script
    decompress(basedir)

    assert os.path.isfile(file1)  # Should have been compressed
    assert os.path.isfile(file2)  # Should not have been compressed
    assert os.path.isfile(file3)  # Should have beend compressed

    assert os.stat(file1).st_size > 1024*79
    assert os.stat(file2).st_size > 1024*49
    assert os.stat(file3).st_size > 1024*99
