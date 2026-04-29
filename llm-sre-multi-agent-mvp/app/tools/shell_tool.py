import subprocess

from app.config import settings


class ShellTool:
    def run(self, script: str) -> dict:
        if not settings.enable_shell_execution:
            return {
                "success": False,
                "message": "Shell execution is disabled. Set ENABLE_SHELL_EXECUTION=true to enable.",
                "stdout": "",
                "stderr": "",
            }

        process = subprocess.run(script, shell=True, capture_output=True, text=True)
        return {
            "success": process.returncode == 0,
            "message": "executed",
            "stdout": process.stdout,
            "stderr": process.stderr,
        }
