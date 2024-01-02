"""
Created on 02.10.2023
"""

import argparse

from pathlib import Path
from sys import argv


def superdiff(original_file: str | Path, modified_file: str | Path, output_file: str | Path = "") -> None:
    """Outputs a file containing all the changes that has been made between the original and modified file.
    Each line in the output file has either a '0 ', '+ ', or '- ' in front meaning respectively no changes,
    added line, deleted line.

    Parameters:
        original_file (str or pathlib.Path): relative or absolute path to the original file.
        modified_file (str or pathlib.Path): relative or absolute path to the modified file to compare against
                                                the original.
        output_file (str or pathlib.Path): relative or absolute path to store the output file.

    Returns:
        None
    """

    org_file = Path(original_file).resolve()
    mod_file = Path(modified_file).resolve()

    # Check if files exist and are files
    if not org_file.is_file():
        raise FileNotFoundError(f"Input original path is not an existing file, got '{org_file}'")
    if not mod_file.is_file():
        raise FileNotFoundError(f"Input modified path is not an existing file, got '{mod_file}'")

    # Inherit default output file from modified file
    if not output_file:
        out_file = Path(f"{mod_file.stem}_superdiff{mod_file.suffix}")
    else:
        out_file = Path(output_file)

    with org_file.open("r") as f_org, mod_file.open("r") as f_mod:
        org_lines = f_org.readlines()
        mod_lines = f_mod.readlines()

        # Files not equal, find changes
        if org_lines != mod_lines:
            out_lines = []
            for org_line in org_lines:
                # Strip any linebreak at end of line
                org_line = org_line.rstrip("\n")

                # Line is unique to original file; append "-" in front
                if org_line not in mod_lines and (org_line + "\n") not in mod_lines:
                    out_lines.append(f"- {org_line}\n")

                # Line in both files; append "0" in front
                else:
                    out_lines.append(f"0 {org_line}\n")

            for i, mod_line in enumerate(mod_lines):
                # Strip any linebreak at end of line
                mod_line = mod_line.rstrip("\n")

                # Line is unique to modified file; append "+" in front and place at index plus one
                if mod_line not in org_lines and (mod_line + "\n") not in org_lines:
                    out_lines.insert(i + 1, f"+ {mod_line}\n")


        # Files are equal, just copy with no changes ("0 " in front of every line)
        else:
            out_lines = ["0 " + line for line in org_lines]

    # If the modified line did not end with an empty line; remove the linebreak from the last line in the file
    if not mod_lines[-1].endswith("\n"):
        out_lines[-1] = out_lines[-1].rstrip("\n")

    # Save output lines to output file
    with out_file.open("w") as f_out:
        f_out.writelines(out_lines)


def main() -> None:
    """Parses the sys arguments and calls superdiff()"""
    parser = argparse.ArgumentParser(
            prog="superdiff",
            description="Compares two files line by line, finds the minimal difference. "
                        "Appends a '0' before an unmodified line,"
                        " a '-' before a deleted line,"
                        " and a '+' before an added line.")

    # Required positional arguments: filenames
    parser.add_argument(
            "original_file",
            help="The original file path to compare against.")

    parser.add_argument(
            "modified_file",
            help="The modified file to compare to the original.")

    # Optional output filename argument:
    parser.add_argument(
            "-o", "--out",
            help="The output filename, defaults to appending '_superdiff' to the filename (before the extension).")

    # Parse the arguments
    args = parser.parse_args(argv[1:])
    forg = Path(args.original_file).resolve()
    fmod = Path(args.modified_file).resolve()
    if args.out:
        fout = Path(args.out).resolve()
    else:
        fout = None

    superdiff(forg, fmod, fout)

if __name__ == "__main__":
    main()

