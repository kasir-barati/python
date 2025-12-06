from os import getenv
from typing import List, TypedDict
import pytest
from unittest.mock import patch, mock_open


def mock_only_secrets() -> list[dict[str, str]]:
    results: list[dict[str, str]] = []

    with open("/tmp/example.txt", "r") as file:
        content = file.read()
        results.append({"normal file": content})

    with open(f"/run/secrets/{getenv("API_KEY_FILE")}", "r") as file:
        api_key = file.read().strip()
        results.append({"secret file": api_key})

    return results


class Secret(TypedDict):
    env: str
    filename: str
    value: str


def should_mock(filename: str) -> bool:
    return filename.startswith("/run/secrets/")


@pytest.fixture(autouse=True)
def mock_secrets(monkeypatch: pytest.MonkeyPatch):
    vars: List[Secret] = [
        {"env": "API_KEY_FILE", "filename": "v1_api_key", "value": "super-secret-key"}
    ]
    file_mapping = {f"/run/secrets/{var['filename']}": var["value"] for var in vars}

    for var in vars:
        monkeypatch.setenv(var["env"], var["filename"])

    original_open = open

    def file_side_effect(file_path: str, *args, **kwargs):
        if should_mock(file_path) and file_path in file_mapping:
            return mock_open(read_data=file_mapping[file_path]).return_value

        return original_open(file_path, *args, **kwargs)

    # Patch the built-in open function
    with patch("builtins.open", side_effect=file_side_effect):
        yield


def test_should_mock_only_secrets():
    res = mock_only_secrets()

    assert len(res) == 2
    assert res[0] == {"normal file": "This is an example file.\n"}
    assert res[1] == {"secret file": "super-secret-key"}
