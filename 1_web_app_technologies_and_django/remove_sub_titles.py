from os import listdir
from os import remove
from os.path import isfile
from os.path import join

"""
Motivation/Philosophy behind this script:
    - I was seek of too many subtitles and TBH ATM - 2022-07-03 - I 
    just wanted to learn English and Germany. So I decided to get rid of them by
    This little beautiful lovely python script
    - I was doing it by hand but it was too tedium and boring to the death
    Besides it was too much error prone.
"""

def main(path: str) -> None:
    files_name: list[str] = listdir(path)
    keep_these_extensions: list[str] = ['.de.srt', '.en.srt', '.mp4']

    # Keep any file with any extension in the list except the predefined list
    files_name = [
        filename for filename in files_name if not any(extension in filename for extension in keep_these_extensions)
    ]

    files_full_path: list[str] = [
        join(path, filename) for filename in files_name
    ]
    
    # Final prof that my script works as it should
    [print(filename) for filename in files_name]

    for file_path in files_full_path:
        if isfile(file_path):
            remove(file_path)


main(
    "/mnt/MyPassport/MyPassportUltra/Learn every day/Python/Django/Coursera - Django for Everybody Specialization 2021-2/3. Django Features and Libraries"
)