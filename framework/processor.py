import os
import subprocess
from framework.execution_result import (
    SuccessfulCompilation,
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

    def __init__(self, name : str, options : [str]) -> None:
        self.name = name
        self.options = options
        # TODO:
        #   * add/lookup default flags if none provided
        #   * lookup C companion processor
        #   * lookup mapping between features and additional flags, or environment variables

    def execute(
            self,
            files : [str],
            location : str,
            features : [str],
            other_files : [str],
            cmd_line_args : [str],
            std_in : str,
            env_vars : {str : str},
            num_images : int,
            run_executable : bool
            ):
        # TODO:
        #  * look at features to determine any extra flags or environment variables needed
        exe_name = os.path.splitext(files[-1])[0] + ".exe"
        object_names = [file + ".o" for file in files]
        stdout = ""
        stderr = ""
        env = dict(os.environ.copy(), **env_vars)
        for src, obj in zip(files, object_names):
            res = subprocess.run(
                [self.name, "-c"] + self.options + [src, "-o", obj],
                cwd=location,
                env=env,
                capture_output=True,
                text=True)
            stdout += res.stdout
            stderr += res.stderr
            if res.returncode != 0: return ExecutionResult(CompilationFailed(), stdout, stderr)
        subprocess.run(
            [self.name] + object_names + ["-o", exe_name],
            cwd=location,
            env=env,
            capture_output=True,
            text=True)
        stdout += res.stdout
        stderr += res.stderr
        if res.returncode != 0: return ExecutionResult(CompilationFailed(), stdout, stderr)
        if run_executable:
            try:
                res = subprocess.run(
                    ["./{exe}".format(exe = exe_name)] + cmd_line_args,
                    cwd=location,
                    env=env,
                    input=std_in,
                    capture_output=True,
                    text=True,
                    timeout=10)
            except:
                return ExecutionResult(ExecutionTimeout(), stdout, stderr)
            stdout += res.stdout
            stderr += res.stderr
            if res.returncode != 0:
                return ExecutionResult(ErrorTermination(res.returncode), stdout, stderr)
            else:
                return ExecutionResult(NormalTermination(), stdout, stderr)
        else:
            return ExecutionResult(SuccessfulCompilation(), stdout, stderr)
