"""Module containing functions used to achieve the desired restructuring of the pollution_data directory
"""
# Include the necessary packages here
import os

from pathlib import Path
from typing import Dict, List


def get_diagnostics(dir: str | Path) -> Dict[str, int]:
    """Get diagnostics for the directory tree, with root directory pointed to by dir.
       Counts up all the files, subdirectories, and specifically .csv, .txt, .npy, .md and other files in the whole directory tree.

    Parameters:
        dir (str or pathlib.Path) : Absolute path to the directory of interest

    Returns:
        res (Dict[str, int]) : a dictionary of the findings with following keys: files, subdirectories, .csv files, .txt files, .npy files, .md files, other files.
    """

    # Dictionary to return
    res = {
        "files": 0,
        "subdirectories": 0,
        ".csv files": 0,
        ".txt files": 0,
        ".npy files": 0,
        ".md files": 0,
        "other files": 0,
    }

    # Convert to Path
    dir = Path(dir)

    # Check exists and directory
    if not dir.exists():
        raise NotADirectoryError(f"Path 'dir' does not exist ('{dir}').")
    if not dir.is_dir():
        raise NotADirectoryError(f"Path 'dir' must be a directory ('{dir}').")

    # List of the specific file extensions for looping
    file_types = ["csv", "txt", "npy", "md"]

    # Count total files
    res["files"] = len(list(dir.rglob("*.*")))

    # Count specific and other files:
    other_count = res["files"]
    for file_type in file_types:
        type_count = len(list(dir.rglob(f"*.{file_type}")))
        res[f".{file_type} files"] += type_count
        other_count -= type_count  # removes these specific file types from the count of other_files
    res["other files"] = other_count

    # Count subdirectories by subtracting the total no. elements with total counted no. files
    total_elements = len(list(dir.rglob("*")))
    res["subdirectories"] = total_elements - res["files"]

    return res


def display_diagnostics(dir: str | Path, contents: Dict[str, int]) -> None:
    """Display diagnostics for the directory tree, with root directory pointed to by dir.
        Objects to display: files, subdirectories, .csv files, .txt files, .npy files, .md files, other files.

    Parameters:
        dir (str or pathlib.Path) : Absolute path the directory of interest
        contents (Dict[str, int]) : a dictionary of the same type as return type of get_diagnostics, has the form:

            .. highlight:: python
            .. code-block:: python

                {
                    "files": 0,
                    "subdirectories": 0,
                    ".csv files": 0,
                    ".txt files": 0,
                    ".npy files": 0,
                    ".md files": 0,
                    "other files": 0,
                }

    Returns:
        None
    """

    # Convert to path
    dir = Path(dir).resolve()  # get absolute path for the path printing

    # Check dir exists and directory
    if not dir.exists():
        raise NotADirectoryError(f"Path does not exist ('{dir}').")
    if not dir.is_dir():
        raise NotADirectoryError(f"Path must be a directory ('{dir}').")

    # Check contents type
    if not isinstance(contents, dict):
        raise TypeError(f"Argument 'contents' {contents.__class__} must be of type dict.")

    # Print the summary to the terminal
    title = f"Diagnostics for '{dir}':"
    print(title)
    print("-" * len(title))  # add seperator lines with same length as title
    print(f"Number of files: {contents['files']}")
    print(f"Number of folders: {contents['subdirectories']:}")
    print(f"Number of .csv files: {contents['.csv files']}")
    print(f"Number of .txt files: {contents['.txt files']}")
    print(f"Number of .npy files: {contents['.npy files']}")
    print(f"Number of .md files: {contents['.md files']}")
    print(f"Number of other files: {contents['other files']}")
    print("-" * len(title))


def display_directory_tree(dir: str | Path, maxfiles: int = 3) -> None:
    """Display a directory tree, with root directory pointed to by dir.
       Limit the number of files to be displayed for convenience to maxfiles.
       This tree is built with inspiration from the code written by "Flimm" at https://stackoverflow.com/questions/6639394/what-is-the-python-way-to-walk-a-directory-tree

    Parameters:
        dir (str or pathlib.Path) : Absolute path to the directory of interest
        maxfiles (int) : Maximum number of files to be displayed at each level in the tree, default to three.

    Returns:
        None

    """

    # Convert to Path
    dir = Path(dir)

    # Check dir exists and directory
    if not dir.exists():
        raise NotADirectoryError(f"Path does not exist ('{dir}').")
    if not dir.is_dir():
        raise NotADirectoryError(f"Path must be a directory ('{dir}').")

    # Check maxfiles
    if not isinstance(maxfiles, int):
        raise TypeError(f"'maxfiles' {maxfiles.__class__} must be of type int.")
    if maxfiles < 1:
        raise ValueError("")

    tab = " " * 3  # 3 spaces indent for each level

    # First print root directory, then files in root directory, then subdirectories and their contents
    # Credit to dhobbs: https://stackoverflow.com/a/9728478
    for root, dirs, files in os.walk(dir):
        level = root.replace(str(dir), '').count(os.sep)
        if level == 0:
            indent = tab * level
        else:
            indent = tab * level + " -"
        print(indent, Path(root).absolute().stem + "/")
        subindent = tab * (level + 1) + " -"
        for count, f in enumerate(files):
            if count >= maxfiles:  # Stop at given max amount of files per subdirectory
                print(subindent, "...")
                break
            print(subindent, f)


def is_gas_csv(path: str | Path) -> bool:
    """Checks if a csv file pointed to by path is an original gas statistics file.
        An original file must be called '[gas_formula].csv' where [gas_formula] is
        in ['CO2', 'CH4', 'N2O', 'SF6', 'H2']. Case insensitive.

    Parameters:
         - path (str of pathlib.Path) : Absolute path to .csv file that will be checked

    Returns
         - (bool) : Truth value of whether the file is an original gas file
    """

    # Convert to Path
    path = Path(path)

    # Check path is a .csv file
    if path.suffix != ".csv":
        raise ValueError(f"Path 'path' must be of file type .csv ('{path}').")

    # List of greenhouse gasses, correct filenames in front of a .csv ending
    gasses = ["CO2", "CH4", "N2O", "SF6", "H2"]
    return path.stem.upper() in gasses  # Checks if filename is one of the gasses, not case-sensitive


def get_dest_dir_from_csv_file(dest_parent: str | Path, file_path: str | Path) -> Path:
    """Given a file pointed to by file_path, derive the correct gas_[gas_formula] directory name.
        Checks if a directory "gas_[gas_formula]", exists and if not, it creates one as a subdirectory under dest_parent.

        The file pointed to by file_path must be a valid file. A valid file must be called '[gas_formula].csv' where [gas_formula]
        is in ['CO2', 'CH4', 'N2O', 'SF6', 'H2'].

    Parameters:
        - dest_parent (str or pathlib.Path) : Absolute path to parent directory where gas_[gas_formula] should/will exist
        - file_path (str or pathlib.Path) : Absolute path to file that gas_[gas_formula] directory will be derived from

    Returns:
        - (pathlib.Path) : Absolute path to the derived directory

    """
    # convert to Path
    dest_parent = Path(dest_parent)
    file_path = Path(file_path)

    # Check correct file_path inputs
    if not file_path.is_file():
        raise ValueError(f"Path 'file_path' must be a file ('{file_path}').")
    if not is_gas_csv(file_path):
        raise ValueError(f"Path 'file_path' must be an original .csv file ('{file_path}').")

    # Check correct dest_parent input
    if not dest_parent.exists():
        raise NotADirectoryError(f"Path 'dest_parent' must exist ('{dest_parent}').")
    if not dest_parent.is_dir():
        raise NotADirectoryError(f"Path 'dest_parent' must be a directory ('{dest_parent}').")

    # Create destination directory absolute path
    dest_path = dest_parent.resolve() / f"gas_{file_path.stem.upper()}"

    # Check if the directory already exists, and create one of not
    if dest_path.exists():
        return dest_path

    Path.mkdir(dest_path)
    return dest_path

def merge_parent_and_basename(path: str | Path) -> str:
    """This function merges the basename and the parent-name of a path into one, uniting them with "_" character.
       It then returns the basename of the resulting path.

    Parameters:
        - path (str or pathlib.Path) : Absolute path to modify

    Returns:
        - new_base (str) : New basename of the path
    """

    # Convert to Path
    path = Path(path)

    # Check if path contains both filename and parent-name
    levels = str(path).split(os.sep)
    if sum(bool(level) for level in levels) < 2:  # counts nonempty elements in list
        raise ValueError(f"Path 'path' must contain both a filename and parent-name ({path}).")

    # New, merged, basename of the path, which will be the new filename
    # Merges the last two path levels by an underscore
    return "_".join(levels[-2:])

def delete_directories(path_list: List[str | Path]) -> None:
    """Prompt the user for permission and delete the objects pointed to by the paths in path_list if
       permission is given. If the object is a directory, its whole directory tree is removed.

    Parameters:
        - path_list (List[str | Path]) : a list of absolute paths to all the objects to be removed.


    Returns:
    None
    """
    # NOTE: This is an optional task, no points assigned. If you are skipping it, remove `raise NotImplementedError` in the function body
    raise NotImplementedError("Remove me if you implement this optional task")

    ...


def safe_mkdir(dir: str | Path) -> None:
    """Attempts to create given directory path. If directory already exists, ask the user to overwrite or to cancel.

    Parameters:
        - dir (str or pathlib.Path) : absolute or relative path to the directory to create

    Returns:
    None
    """

    # Convert to path
    work_dir = Path(dir).resolve()  # get absolute path

    try:
        Path.mkdir(dir)
    except FileExistsError:  # Ask user to overwrite existing by_gas directory or cancel
        print(f"Directory '{dir}' already exists. Overwrite it? (Y/N)")
        if input("$ ").upper() == "Y":
            print(f"Overwriting directory '{dir}'...")
            Path.mkdir(dir, exist_ok=True)
        else:
            print("Cancelling...")
            exit()