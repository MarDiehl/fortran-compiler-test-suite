import os
import subprocess
import pathlib
import yaml
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

    def __init__(self, processor : str, c_processor : str, options : [str]) -> None:
        compiler_configurations = yaml.safe_load(open(os.path.join("framework", "compiler_configurations.yml"), 'r'))
        self.processor = processor
        proc_config = None
        for proc in compiler_configurations.keys():
            # This should work for most cases where even a full path
            # and/or version is specified for the compiler
            # (i.e. /usr/bin/gfortran-13)
            if proc in processor:
                proc_config = compiler_configurations[proc]
                break
        if proc_config is not None:
            if c_processor == "":
                self.c_processor = proc_config["c_compiler"]
            else:
                self.c_processor = c_processor
            if len(options) == 0:
                self.options = proc_config["default_flags"]
            else:
                self.options = options
            self.feature_flags = proc_config.get("feature_flags", dict())
        else:
            if c_processor == "":
                # just assume they want gcc if they didn't specify and
                # we don't recognize the Fortran compiler
                self.c_processor = "gcc"
            else:
                self.c_processor = c_processor
            self.options = options
            self.feature_flags = dict()

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
            if pathlib.Path(src).suffix == ".c":
                res = subprocess.run(
                    [self.c_processor, "-c"] + [src, "-o", obj],
                    cwd=location,
                    env=env,
                    capture_output=True,
                    text=True)
            else:
                res = subprocess.run(
                    [self.processor, "-c"] + self.options + [src, "-o", obj],
                    cwd=location,
                    env=env,
                    capture_output=True,
                    text=True)
            stdout += res.stdout
            stderr += res.stderr
            if res.returncode != 0: return ExecutionResult(CompilationFailed(), stdout, stderr)
        subprocess.run(
            [self.processor] + object_names + ["-o", exe_name],
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
