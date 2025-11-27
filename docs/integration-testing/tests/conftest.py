"""
Pytest configuration and fixtures shared across all test files.
"""

import sys
from pathlib import Path

# Add src directory to Python path so tests can import from src modules
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Automatically discover all fixture files
fixture_files = []
tests_dir = Path(__file__).parent  # Gets the tests/ directory
for file in tests_dir.glob("*_fixture.py"):
    if file.name != "__init__.py":
        fixture_files.append(file.stem)  # Get filename without extension

# Register the fixture module so pytest can discover fixtures
pytest_plugins = fixture_files
