import os
import subprocess
from framework.execution_result import (
    CompilationFailed,
    ExecutionTimeout,
    ErrorTermination,
    NormalTermination,
    ExecutionResult
    )

class Processor:
    """
    The base/default implementation for a Fortran processor
    """

    def __init__(self, name, options) -> None:
        self.name = name
        self.options = options
        # TODO:
        #   * add/lookup default flags if none provided
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
        #  * add command line arguments to program invocation
        #  * feed std_in to executing program
        #  * set environment variables prior to compilation and execution
        #  * look at features to determine any extra flags or environment variables needed
        exe_name = os.path.splitext(files[-1])[0] + ".exe"
        object_names = [file + ".o" for file in files]
        stdout = b""
        stderr = b""
        for src, obj in zip(files, object_names):
            res = subprocess.run(
                [self.name, "-c"] + self.options + [src, "-o", obj],
                cwd=location,
                capture_output=True)
            stdout += res.stdout
            stderr += res.stderr
            if res.returncode != 0: return ExecutionResult(CompilationFailed(), stdout, stderr)
        subprocess.run(
            [self.name] + object_names + ["-o", exe_name],
            cwd=location,
            capture_output=True)
        stdout += res.stdout
        stderr += res.stderr
        if res.returncode != 0: return ExecutionResult(CompilationFailed(), stdout, stderr)
        try:
            res = subprocess.run(
                ["./{exe}".format(exe = exe_name)],
                cwd=location,
                capture_output=True,
                timeout=10)
        except:
            return ExecutionResult(ExecutionTimeout(), stdout, stderr)
        stdout += res.stdout
        stderr += res.stderr
        if res.returncode != 0:
            return ExecutionResult(ErrorTermination(res.returncode), stdout, stderr)
        else:
            return ExecutionResult(NormalTermination(), stdout, stderr)
