from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def test_required_directories_exist() -> None:
    expected_directories = [
        "metadata",
        "mcp_commands",
        "service",
        "docs",
        "infrastructure",
        "shared",
        "tests",
    ]

    for directory in expected_directories:
        path = ROOT / directory
        assert path.exists() and path.is_dir(), f"Missing required directory: {directory}"


def test_required_files_exist() -> None:
    expected_files = ["pyproject.toml", "Makefile", "README.md"]

    for file_name in expected_files:
        path = ROOT / file_name
        assert path.exists(), f"Missing required file: {file_name}"
