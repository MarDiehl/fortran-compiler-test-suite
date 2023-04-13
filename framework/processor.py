import os

class Processor:
    """
    The base/default implementation for a Fortran processor
    """

    def __init__(self, name) -> None:
        self.name = name

    def execute(self, file, location):
        orig_path = os.curdir
        exe_name = os.path.splitext(file)[0] + ".exe"
        os.chdir(location)
        os.system("{processor} {source} -o {exe} && ./{exe}".format(processor = self.name, source = file, exe = exe_name))
        os.chdir(orig_path)