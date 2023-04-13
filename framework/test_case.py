import os

class TestCase:
    """
    The base/default implementation for a test case
    """
    def __init__(self, file, location):
        self.file = file
        self.location = location

    def execute(self):
        orig_path = os.curdir
        exe_name = os.path.splitext(self.file)[0] + ".exe"
        os.chdir(self.location)
        os.system("gfortran {0} -o {1} && ./{1}".format(self.file, exe_name))
        os.chdir(orig_path)