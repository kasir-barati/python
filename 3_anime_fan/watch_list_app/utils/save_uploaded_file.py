import os
from pathlib import Path
from typing import NoReturn
from django.core.files import File
from shared.random_string import random_string


def random_filename(
        original_filename: str,
        suffix: str = '') -> str:
    original_filename = original_filename.strip()
    suffix = suffix.strip()
    filename, extension = os.path.splitext(
        original_filename,
    )
    generated_filename = \
        random_string(20) \
        + '_' \
        + filename \
        + suffix \
        + extension

    return generated_filename


def save_uploaded_file(
        absolute_path: str,
        file: File,) -> None|NoReturn:
    # Just due to what I read, assertive programming is for things
    # that we think never ever happen
    assert os.path.isabs(absolute_path),\
        "The passed path is not absolute path!"

    Path(absolute_path).parent.mkdir(
        exist_ok=True, 
        parents=True,
    )

    # w+ to create and then open file in write mode
    with open(absolute_path, 'wb+') as destination_file:
        """
        Looping over UploadedFile.chunks() instead of using read()
        ensures that large files don’t overwhelm your system’s memory.
        """
        [destination_file.write(chunk) for chunk in file.chunks()]

