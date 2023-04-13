import os

class Processor:
    """
    The base/default implementation for a Fortran processor
    """

    def __init__(self, name) -> None:
        self.name = name

    def execute(self, files, location):
        orig_path = os.curdir
        exe_name = os.path.splitext(files[-1])[0] + ".exe"
        os.chdir(location)
        os.system("{processor} {source} -o {exe} && ./{exe}".format(processor = self.name, source = files[0], exe = exe_name))
        os.chdir(orig_path)