"""
Created on 15.09.2023
Exercise 2: https://pages.github.uio.no/IN3110/assignments/exercises/week3.html
"""

from sys import argv, exit
from pathlib import Path

def find(extension: str | Path, directory: str | Path) -> list[Path]:
    """Returns all files with given extension in a given parent directory and its subdirectories.

    Parameters:
        - extension (str or pathlib.Path) : file extension to search for.
        - directory (str or pathlib.Path) : parent directory to search in for files.

    Returns:
        - (list) : list containing pathlib.Path paths to all found files.
    """

    # Convert to absolute Path
    dir = Path(directory).resolve()

    # Check valid directory
    if not dir.is_dir():
        raise NotADirectoryError(f"Given directory path 'directory' must be an existing directory ('{dir}').")

    # Add a dot to the extension if it doesnt exist
    if "." not in extension:
        extension = "." + extension

    # convert absolute paths back to relative paths for the given directory input
    paths = dir.rglob(f"*{extension}")
    relative_paths = [Path(str(path) [str(path).index(str(dir)) + len(str(dir)):] ) for path in paths]
    return relative_paths


if __name__ == "__main__":
    if len(argv) < 3:  # arguments not gotten
        print("Usage:\n  python find.py <file extension> <directory path to search>")
        print("Example:\n  python find.py .py .")
        exit(0)
    paths = find(argv[1], argv[2])
    print(*paths, sep="\n")  # print all files on seperate line
