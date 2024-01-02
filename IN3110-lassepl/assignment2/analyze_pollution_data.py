"""This is the mane script orchestrating the restructuring and plotting of the content of the pollution_data directory.
"""

# Import necessary packages here
from pathlib import Path
from shutil import copyfile, rmtree

from analytic_tools.utilities import (
    merge_parent_and_basename,
    get_dest_dir_from_csv_file,
    is_gas_csv,
    get_diagnostics,
    display_diagnostics,
    display_directory_tree,
    safe_mkdir
)
from analytic_tools.plotting import plot_pollution_data


def restructure_pollution_data(pollution_dir: str | Path, dest_dir: str | Path) -> None:
    """This function searches the tree of pollution_data directory pointed to by pollution_dir for .csv files
        that satisfy the criteria described in the assignment. It then moves a renamed copy of these files to gas-specific
        sub-directories in dest_dir, which will be created based on the gasses present in pollution_data directory.

    Parameters:
        - pollution_dir (str or pathlib.Path) : The absolute path to pollution_data directory
        - dest_dir (str or pathlib.Path) : The absolute path to new directory where gas-specific subdirectories will
                                     be created, which must be pollution_data_restructured/by_gas

    Returns:
    None

    Pseudocode:
    1. Iterate through the contents of `pollution_dir`
    2. Find valid .csv files for gasses ([`[gas_formula].csv` files of correct gas types).
    3. Create/assign new directory to store them under `dest_dir` using `get_dest_dir_from_csv_file`
    4. Assign a new name using `merge_parent_and_basename` and copy the file to the new destination.
       If the file happens already to exist there, it should be overwritten.
    """

    # Convert to path
    pollution_dir = Path(pollution_dir)
    dest_dir = Path(dest_dir)

    # Check paths exists and are to directories
    if not pollution_dir.exists() or not pollution_dir.is_dir():
        raise NotADirectoryError(f"Path 'pollution_dir' must be an existing directory path ({pollution_dir}.")
    if not dest_dir.exists() or not dest_dir.is_dir():
        raise NotADirectoryError(f"Path 'dest_dir' must be an existing directory path ({dest_dir}.")

    # Contents of pollution_data tree
    contents = pollution_dir.rglob("*.*")

    for path in contents:
        if path.suffix != ".csv":  # skip if not .csv file
            continue
        if not is_gas_csv(path):  # skip if not an original gas .csv file
            continue
        gas_dest = get_dest_dir_from_csv_file(dest_dir, path) / merge_parent_and_basename(path)  # new absolute filename
        copyfile(path, gas_dest)  # Copies the file and overwrites if it already exists


def analyze_pollution_data(work_dir: str | Path) -> None:
    """Do the restructuring of the pollution_data and plot
       the statistics showing emissions of each gas as function of all the corresponding
       sources. The new structure and the plots are saved in a separate directory under work_dir

    Parameters:
        - work_dir (str or pathlib.Path) : Absolute path to the working directory that
                                    contains the pollution_data directory and where the new directories will be created

    Returns:
    None

    Pseudocode:
    - Create pollution_data_restructured in work_dir
    - Populate it with a by_gas subdirectory
    - Make a call to restructure_pollution_data
    - Populate pollution_data_restructured with a subdirectory named figures
    - Make a call to plot_pollution_data
    """

    # Convert to path
    work_dir = Path(work_dir)

    # Check work_dir is existing directory
    if not work_dir.exists() or not work_dir.is_dir():
        raise NotADirectoryError(f"Path 'pollution_dir' must be an existing directory path ({work_dir}.")

    pollution_dir = work_dir / "pollution_data"

    # Display pollution_dir diagnostics and directory tree
    display_diagnostics(work_dir, get_diagnostics(work_dir))
    display_directory_tree(work_dir)

    # Create pollution_data_restructured in work_dir
    restructured_dir = work_dir / "pollution_data_restructured"
    safe_mkdir(restructured_dir)

    # Populate it with a by_gas sub-folder
    by_gas_dir = restructured_dir / "by_gas"
    safe_mkdir(by_gas_dir)

    # Restructure the gas files in the new restructured_dir
    restructure_pollution_data(pollution_dir, by_gas_dir)

    # Populate pollution_data_restructured with a sub folder named figures
    figures_dir = restructured_dir / "figures"
    safe_mkdir(figures_dir)

    # Plot the pollution data
    plot_pollution_data(by_gas_dir, figures_dir)


def analyze_pollution_data_tmp(work_dir: str | Path) -> None:
    """Do the restructuring of the pollution_data in a temporary directory and create the figures
       showing emissions of each gas as function of all the corresponding
       sources. The new figures are saved in a real directory under work_dir.

    Parameters:
        - work_dir (str or pathlib.Path) : Absolute path to the working directory that
                                    contains the pollution_data directory and where the figures will be saved

    Returns:
    None

    Pseudocode:
    - Create a temporary directory and copy pollution_data directory to it
    - Perform the same operations as inA analyze_pollution_data
    - Copy (or directly save) the figures to a directory named `figures` under the original working directory pointed to by `work_dir`
    """

    # Convert to path
    work_dir = Path(work_dir)

    # Check work_dir is existing directory
    if not work_dir.exists() or not work_dir.is_dir():
        raise NotADirectoryError(f"Path 'pollution_dir' must be an existing directory path ({work_dir}.")

    pollution_dir = work_dir / "pollution_data"

    # Display pollution_dir diagnostics and directory tree
    display_diagnostics(work_dir, get_diagnostics(work_dir))
    display_directory_tree(work_dir)

    # Create a temporary temp_pollution_data_restructured in work_dir
    restructured_temp_dir = work_dir / "pollution_data_restructured_temp"
    safe_mkdir(restructured_temp_dir)

    # Populate it with a by_gas sub-folder
    by_gas_dir = restructured_temp_dir / "by_gas"
    safe_mkdir(by_gas_dir)

    # Restructure the gas files in the new temp_restructured_temp_dir
    restructure_pollution_data(pollution_dir, by_gas_dir)

    # Create a permanent figures directory under work_dir to store the plots
    figures_dir = work_dir / "figures"
    safe_mkdir(figures_dir)

    # Plot the pollution data
    plot_pollution_data(by_gas_dir, figures_dir)

    # Delete the entire temp directory tree
    rmtree(restructured_temp_dir)


if __name__ == "__main__":
    work_dir = "."
    analyze_pollution_data(Path(work_dir).resolve())
