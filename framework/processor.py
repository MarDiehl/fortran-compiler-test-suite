import os

class Processor:
    """
    The base/default implementation for a Fortran processor
    """

    def __init__(self, name) -> None:
        self.name = name
        # TODO:
        #   * add/lookup default flags
        #   * lookup C companion processor
        #   * lookup mapping between features and additional flags, or environment variables

    def execute(
            self,
            files,
            location,
            features,
            other_files,
            cmd_line_args,
            std_in,
            env_vars,
            num_images
            ):
        # TODO:
        #  * detect compilation and/or link failures and record their screen output
        #  * record screen output from program execution
        #  * add command line arguments to program invocation
        #  * feed std_in to executing program
        #  * set environment variables prior to compilation and execution
        #  * determine if program stopped with normal or error termination
        #  * look at features to determine any extra flags or environment variables needed
        orig_path = os.curdir
        exe_name = os.path.splitext(files[-1])[0] + ".exe"
        object_names = [file + ".o" for file in files]
        os.chdir(location)
        for src, obj in zip(files, object_names):
            os.system("{processor} -c {source} -o {object}".format(processor = self.name, source = src, object = obj))
        os.system("{processor} {objects} -o {exe}".format(processor = self.name, objects = " ".join(object_names), exe = exe_name))
        os.system("./{exe}".format(exe = exe_name))
        os.chdir(orig_path)