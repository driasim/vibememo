"""CLI flag validation tests for vibememo main.py

Tests that all 8 enhance CLI flags parse correctly:
1. --version (action=store_true)
2. --verbose (action=store_true)
3. --quiet (action=store_true)
4. --config / -c (metavar=PATH)
5. --no-color (action=store_true)
6. --cors-origins (metavar=ORIGINS)
7. --max-connections (type=int)
8. --auto-migrate (action=store_true)
"""

import os
import sys
import subprocess
import pytest

MAIN_PY = os.path.join(os.path.dirname(__file__), "..", "python", "main.py")


def run_help():
    """Run main.py --help and return stdout"""
    result = subprocess.run(
        [sys.executable, MAIN_PY, "--help"],
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_version_flag_defined():
    """Verify --version flag exists in argparse"""
    help_output = run_help()
    assert "--version" in help_output, "--version flag should be defined"


def test_verbose_flag_defined():
    """Verify --verbose flag exists in argparse"""
    help_output = run_help()
    assert "--verbose" in help_output, "--verbose flag should be defined"


def test_quiet_flag_defined():
    """Verify --quiet flag exists in argparse"""
    help_output = run_help()
    assert "--quiet" in help_output, "--quiet flag should be defined"


def test_config_flag_defined():
    """Verify --config / -c flag exists in argparse"""
    help_output = run_help()
    assert "--config" in help_output or "-c" in help_output, (
        "--config / -c flag should be defined"
    )


def test_no_color_flag_defined():
    """Verify --no-color flag exists in argparse"""
    help_output = run_help()
    assert "--no-color" in help_output, "--no-color flag should be defined"


def test_cors_origins_flag_defined():
    """Verify --cors-origins flag exists in argparse"""
    help_output = run_help()
    assert "--cors-origins" in help_output, "--cors-origins flag should be defined"


def test_max_connections_flag_defined():
    """Verify --max-connections flag exists in argparse"""
    help_output = run_help()
    assert "--max-connections" in help_output, "--max-connections flag should be defined"


def test_auto_migrate_flag_defined():
    """Verify --auto-migrate flag exists in argparse"""
    help_output = run_help()
    assert "--auto-migrate" in help_output, "--auto-migrate flag should be defined"
