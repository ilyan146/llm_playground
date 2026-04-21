import io
import subprocess
import sys
from pathlib import Path

from .config import COMPILE_COMMAND, EXTENSION, RUN_COMMAND, _DIR

def run_python(code: str) -> str:
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer
    try:
        exec(code, {"__builtins__": __builtins__})  # noqa: S102
        return buffer.getvalue()
    except Exception as e:
        return f"Error: {e}"
    finally:
        sys.stdout = old_stdout


def compile_and_run(code: str) -> str:
    (_DIR / f"main.{EXTENSION}").write_text(code)
    try:
        subprocess.run(COMPILE_COMMAND, check=True, text=True, capture_output=True, cwd=_DIR)
        result = subprocess.run(RUN_COMMAND, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred:\n{e.stderr}"
