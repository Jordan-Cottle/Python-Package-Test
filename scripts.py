import os

from os.path import abspath, join, dirname

os.environ["PYTHONPATH"] = join(dirname(abspath(__file__)))

print(os.environ["PYTHONPATH"])


def run(command, check=True):
    """Run a system command and assert it succeeded."""

    exit_code = os.system(command)

    if check and exit_code != 0:
        raise RuntimeError(f"{command} failed to execute with exit code {exit_code}")

    return exit_code


def run_tests():
    """Run all tests."""

    run("pytest --cov")
