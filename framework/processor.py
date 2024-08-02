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
        exe_name = os.path.splitext(files[-1])[0] + ".exe"
        object_names = [file + ".o" for file in files]
        commands = []
        stdout = ""
        stderr = ""
        env = dict(os.environ.copy(), **env_vars)
        opts = self.options.copy()
        for feat in self.feature_flags.keys():
            if feat in features:
                for var, val in self.feature_flags[feat].get("env_vars", dict()).items():
                    env[var] = val.format(num_images=num_images)
                for flag in self.feature_flags[feat].get("flags", []):
                    opts.append(flag.format(num_images=num_images))
        for src, obj in zip(files, object_names):
            if pathlib.Path(src).suffix == ".c":
                cmd = [self.c_processor, "-c"] + [src, "-o", obj]
                commands.append(" ".join(cmd))
                res = subprocess.run(
                    cmd,
                    cwd=location,
                    env=env,
                    capture_output=True,
                    text=True)
            else:
                cmd = [self.processor, "-c"] + opts + [src, "-o", obj]
                commands.append(" ".join(cmd))
                res = subprocess.run(
                    cmd,
                    cwd=location,
                    env=env,
                    capture_output=True,
                    text=True)
            stdout += res.stdout
            stderr += res.stderr
            if res.returncode != 0: return ExecutionResult(commands, CompilationFailed(), stdout, stderr)
        cmd = [self.processor] + opts + object_names + ["-o", exe_name]
        commands.append(" ".join(cmd))
        subprocess.run(
            cmd,
            cwd=location,
            env=env,
            capture_output=True,
            text=True)
        stdout += res.stdout
        stderr += res.stderr
        if res.returncode != 0: return ExecutionResult(commands, CompilationFailed(), stdout, stderr)
        if run_executable:
            try:
                cmd = ["./{exe}".format(exe = exe_name)] + cmd_line_args
                commands.append(" ".join(cmd))
                res = subprocess.run(
                    cmd,
                    cwd=location,
                    env=env,
                    input=std_in,
                    capture_output=True,
                    text=True,
                    timeout=10)
            except:
                return ExecutionResult(commands, ExecutionTimeout(), stdout, stderr)
            stdout += res.stdout
            stderr += res.stderr
            if res.returncode != 0:
                return ExecutionResult(commands, ErrorTermination(res.returncode), stdout, stderr)
            else:
                return ExecutionResult(commands, NormalTermination(), stdout, stderr)
        else:
            return ExecutionResult(commands, SuccessfulCompilation(), stdout, stderr)
