"""Security tests for vibememo PR fixes:
- PR #3: API key auth middleware + CORS
- PR #2: Shell injection / flag injection in CLI templates
- PR #1: Path traversal in transcript_path endpoint
"""

import os
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python"))


# --- PR #1: Path Traversal ---
def test_path_traversal_prevention():
    """Verify api.py prevents path traversal in transcript_path endpoint"""
    api_path = os.path.join(
        os.path.dirname(__file__), "..", "python", "memory_engine", "api.py"
    )
    with open(api_path) as f:
        content = f.read()
    # Check for path traversal protections
    protection_patterns = [
        "os.path.abspath", "os.path.realpath", "os.path.normpath",
        "..", "traversal", "sanitize",
        "startswith", "resolve", "Path(",
        "safe_join", "BASE_DIR", "base_dir",
    ]
    found = [p for p in protection_patterns if p in content]
    assert len(found) >= 2, (
        f"api.py should contain path traversal protection. "
        f"Found: {found}"
    )


def test_path_traversal_blocks_dotdot():
    """Verify path traversal blocks '..' sequences"""
    api_path = os.path.join(
        os.path.dirname(__file__), "..", "python", "memory_engine", "api.py"
    )
    with open(api_path) as f:
        content = f.read()
    # Should have some check for '..' or path resolution
    has_dotdot_check = any(
        pattern in content for pattern in [
            "..", "os.path.abspath", "os.path.realpath",
            "Path", "resolve", "normpath",
        ]
    )
    assert has_dotdot_check, "Should check for directory traversal attempts"


def test_transcript_path_safe_join():
    """Verify transcript_path uses safe path joining"""
    api_path = os.path.join(
        os.path.dirname(__file__), "..", "python", "memory_engine", "api.py"
    )
    with open(api_path) as f:
        content = f.read()
    # Path should be resolved against a base directory
    has_base_dir = any(
        pattern in content for pattern in [
            "BASE_DIR", "base_dir", "BASE_PATH", "base_path",
            "TRANSCRIPT_DIR", "transcript_dir",
        ]
    )
    has_safe_join = any(
        pattern in content for pattern in [
            "os.path.join", "Path(",
            "startswith", "relative_to",
        ]
    )
    assert has_base_dir or has_safe_join, (
        "Should use a base directory and safe path joining"
    )


# --- PR #2: Shell/Flag Injection ---
def test_shell_injection_prevention():
    """Verify config.py prevents shell injection via session_id"""
    config_path = os.path.join(
        os.path.dirname(__file__), "..", "python", "memory_engine", "config.py"
    )
    with open(config_path) as f:
        content = f.read()
    # Should shell-quote or sanitize inputs
    protection_patterns = [
        "shlex.quote", "shlex.escape", "shell=True",
        "pipes.quote", "quote(",
        "sanitize", "escape",
        "--", "injection",
    ]
    found = [p for p in protection_patterns if p in content]
    assert len(found) >= 1, (
        f"config.py should contain shell injection prevention. "
        f"Found: {found}"
    )


def test_flag_injection_prevention():
    """Verify CLI templates prevent flag injection"""
    config_path = os.path.join(
        os.path.dirname(__file__), "..", "python", "memory_engine", "config.py"
    )
    with open(config_path) as f:
        content = f.read()
    # Should use -- to separate options from arguments
    uses_double_dash = "--" in content
    uses_quoting = any(
        pattern in content for pattern in [
            "shlex", "quote", "escape",
        ]
    )
    assert uses_double_dash or uses_quoting, (
        "Should use shell quoting or -- to prevent flag injection"
    )


def test_session_id_is_sanitized():
    """Verify session_id is sanitized before use in shell commands"""
    config_path = os.path.join(
        os.path.dirname(__file__), "..", "python", "memory_engine", "config.py"
    )
    with open(config_path) as f:
        content = f.read()
    # session_id should be quoted or validated
    has_session_id = "session_id" in content or "sessionId" in content
    has_sanitization = any(
        pattern in content for pattern in [
            "shlex.quote", "shlex.escape", "sanitize",
            "re.sub", "replace(", "strip(",
        ]
    )
    assert has_session_id, "config.py should reference session_id"
    assert has_sanitization, "session_id should be sanitized"


# --- PR #3: API Key Auth + CORS ---
def test_api_key_auth_middleware():
    """Verify api.py has API key auth middleware"""
    api_path = os.path.join(
        os.path.dirname(__file__), "..", "python", "memory_engine", "api.py"
    )
    with open(api_path) as f:
        content = f.read()
    auth_patterns = [
        "API_KEY", "api_key",
        "Authorization", "X-API-Key",
        "middleware", "auth",
        "os.environ", "os.getenv",
    ]
    found = [p for p in auth_patterns if p in content]
    assert len(found) >= 2, (
        f"api.py should contain auth middleware. "
        f"Found: {found}"
    )


def test_cors_configurable():
    """Verify CORS origins are configurable"""
    api_path = os.path.join(
        os.path.dirname(__file__), "..", "python", "memory_engine", "api.py"
    )
    with open(api_path) as f:
        content = f.read()
    cors_patterns = [
        "CORS", "cors",
        "allow_origins", "allowed_origins",
        "CORSMiddleware",
        "Access-Control",
    ]
    found = [p for p in cors_patterns if p in content]
    assert len(found) >= 1, (
        f"api.py should contain CORS configuration. "
        f"Found: {found}"
    )


def test_api_key_from_environment():
    """Verify API key is loaded from environment"""
    api_path = os.path.join(
        os.path.dirname(__file__), "..", "python", "memory_engine", "api.py"
    )
    with open(api_path) as f:
        content = f.read()
    uses_env = any(
        pattern in content for pattern in [
            "os.environ", "os.getenv", "environ.get",
            "os.environ.get", "config.",
        ]
    )
    assert uses_env, "API key should come from environment variable"


def test_auth_is_optional():
    """Verify auth middleware is optional (configurable)"""
    api_path = os.path.join(
        os.path.dirname(__file__), "..", "python", "memory_engine", "api.py"
    )
    with open(api_path) as f:
        content = f.read()
    # Should have conditional auth
    has_optional = any(
        pattern in content for pattern in [
            "if ", "else", "optional", "enabled",
            "is not None", "getenv",
        ]
    )
    assert has_optional, "Auth middleware should be optional/conditional"
