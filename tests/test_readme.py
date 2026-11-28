"""Checks that the README keeps the local and Docker troubleshooting guide (task DOC-01)."""
from pathlib import Path

README = (Path(__file__).resolve().parent.parent / "README.md").read_text(encoding="utf-8")


def test_powershell_activation_uses_a_single_backslash_path():
    assert ".venv\\Scripts\\Activate.ps1" in README
    assert ".venv\\\\Scripts" not in README


def test_macos_linux_activation_is_documented():
    assert "source .venv/bin/activate" in README


def test_docker_desktop_must_be_running_on_windows():
    assert "Docker Desktop" in README
    assert "engine is running" in README


def test_docker_connection_error_symptom_and_remedy_are_documented():
    assert "dockerDesktopLinuxEngine" in README
    assert "Open Docker Desktop" in README


def test_endpoints_and_port_mapping_are_documented():
    assert "/health" in README
    assert "/services" in README
    assert "-p 5000:5000" in README
    assert "HOST_PORT:CONTAINER_PORT" in README


def test_troubleshooting_section_exists():
    assert "## Troubleshooting" in README