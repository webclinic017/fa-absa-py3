""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAXVAProcess.py"
import atexit
import os
import subprocess
import traceback

import AAIntegrationUtility

class SynchronousProcess:
    """
    Helper class to execute synchronous external processes.
    """
    def __init__(
        self, name, cwd, exe, args,
        stdout=None, stderr=None, output_files=None,
        env=None, success_check_func=None, cleanup_func=None,
    ):
        self._cmd, self._kwargs = self._getArgs(
            name=name, cwd=cwd, exe=exe, args=args, env=env
        )
        self._stdout = stdout or (lambda msg: None)
        self._stderr = stderr or (lambda msg: None)
        self._output_files_modified_times = self._getModifiedFileTimes(
            output_files=output_files or []
        )
        self._success_check = success_check_func or \
            (lambda output_files, stdout: True)
        self._cleanup = cleanup_func or (lambda: None)

    def run(self):
        try:
            return self._run()
        except:
            self._stderr(traceback.format_exc())

        return False

    def _run(self):
        self._stdout('Executing ' + ' '.join(self._cmd))
        proc = subprocess.Popen(self._cmd, **self._kwargs)
        if proc.pid:
            atexit.register(proc.terminate)

        stdout = []
        for line in iter(proc.stdout.readline, ''):
            line = line.strip()
            self._stdout(line)
            stdout.append(line)

        proc.wait()
        self._cleanup()
        return self._successCheck(stdout=stdout)

    def _getArgs(self, name, cwd, exe, args, env):
        startup_info = subprocess.STARTUPINFO()
        startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startup_info.wShowWindow = subprocess.SW_HIDE
        sp_kwargs = {
            'shell': False,
            'env': env or os.environ,
            'cwd': AAIntegrationUtility.forwardSlashedPath(path=cwd),
            'startupinfo': startup_info,
            'universal_newlines': True,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.STDOUT,
            'stdin': subprocess.PIPE
        }
        exe = AAIntegrationUtility.forwardSlashedPath(path=exe, check=True)
        return [exe] + args, sp_kwargs

    def _getModifiedFileTimes(self, output_files):
        times = {}
        for f in output_files:
            try:
                times[f] = os.path.getmtime(f)
            except:
                times[f] = None

        return times

    def _outputFilesModified(self):
        results = []
        for f, mod_time in list(self._output_files_modified_times.items()):
            try:
                if mod_time:
                    results.append(os.path.getmtime(f) > mod_time)
                else:
                    results.append(os.path.isfile(f))
            except:
                results.append(False)

        return all(results)

    def _successCheck(self, stdout):
        success = self._outputFilesModified() and self._success_check(
            output_files=list(self._output_files_modified_times.keys()),
            stdout=stdout
        )
        return success
