import ast
import subprocess


def calculate(user_input):
    # Parse literals rather than executing arbitrary Python code.
    return ast.literal_eval(user_input)


def run_command():
    # Use a fixed executable and arguments; never pass user input to a shell.
    return subprocess.run(
        ["whoami"],
        shell=False,
        capture_output=True,
        text=True,
        check=False,
        timeout=5
    )