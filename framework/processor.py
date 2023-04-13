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
        object_names = [file + ".o" for file in files]
        os.chdir(location)
        for src, obj in zip(files, object_names):
            os.system("{processor} -c {source} -o {object}".format(processor = self.name, source = src, object = obj))
        os.system("{processor} {objects} -o {exe}".format(processor = self.name, objects = " ".join(object_names), exe = exe_name))
        os.system("./{exe}".format(exe = exe_name))
        os.chdir(orig_path)