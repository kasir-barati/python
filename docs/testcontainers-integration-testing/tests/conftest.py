"""
Pytest configuration and fixtures shared across all test files.
"""

import sys
from pathlib import Path

# Add src directory to Python path so tests can import from src modules
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Add project root to Python path so tests can import from tests package
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Automatically discover all fixture files recursively
fixture_files = []
tests_dir = Path(__file__).parent  # Gets the tests/ directory
for file in tests_dir.rglob("*_fixture.py"):  # rglob for recursive search
    if file.name != "__init__.py":
        # Convert path to module notation (e.g., tests.whatever_fixture)
        relative_path = file.relative_to(project_root)
        module_path = str(relative_path.with_suffix("")).replace("/", ".")
        fixture_files.append(module_path)

# Register the fixture module so pytest can discover fixtures
pytest_plugins = fixture_files
