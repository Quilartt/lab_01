import subprocess
import sys

import pytest


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_01():
    result = run_cli("--help")
    assert result.returncode == 0
    assert "calc" in result.stdout
    assert "convert" in result.stdout


def test_cli_02():
    result = run_cli("calc", "2+3*4")
    assert result.returncode == 0
    assert float(result.stdout.strip()) == pytest.approx(14.0)


def test_cli_03():
    result = run_cli("calc", "1/0")
    assert result.returncode == 2
    assert "DivisionByZero" in result.stderr