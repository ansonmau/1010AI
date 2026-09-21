import sys
import subprocess
import threading

class XCMD:
    def __init__(self):
        pass

    def x(self, command, cwd=None, check=False):
        """Run a terminal command and return (returncode, stdout, stderr)."""
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=False,
            text=True,
        )
        if check and result.returncode != 0:
            raise RuntimeError(f"Command failed ({result.returncode}): {result.stderr.strip()}")
        return result.returncode, result.stdout, result.stderr

    def x_async(self, command, on_done=None, cwd=None):
        def worker():
            result = self.x(command, cwd=cwd)
            if on_done:
                on_done(*result)

        t = threading.Thread(target=worker, daemon=True)
        t.start()
        return t
