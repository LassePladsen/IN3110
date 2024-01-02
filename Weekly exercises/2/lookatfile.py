from os.path import getsize
from sys import argv
from pathlib import Path

path = Path(argv[1]).resolve()
title = f"\nLOOKING AT PATH '{path.stem}{path.suffix}':"

print(title)
print("-" * len(title))  # add seperator lines with same length as title

if not path.exists():
    print("This path does not exist.")

else:
    print(f"Absolute path: '{path}'")

    # FILE/DIR
    if path.is_dir():
        print("This is a directory.")
        # DIR CONTENTS
        print(f"Its contents are: {[subpath.stem+subpath.suffix for subpath in path.glob('*')]}.")

    elif path.is_file():
        print(f"This is a file with extension '{path.suffix}'.")
        # FILE SIZE
        if (size := getsize(path)) < 100:  # less than 0.1 kb
            print(f"Its size is {size:.2f} B.")
        elif 100 <= size < 1_000_000:  # less than 0.1 kb
            print(f"Its size is {size/1000:.2f} KB.")
        elif 1e6 <= size < 1e9:  # greater or equal to 1000 kb
            print(f"Its size is {size/1e6:.2f} MB.")
        elif size >= 1e9:  # greater or equal to 1000 mb
            print(f"Its size is {size/1e9:.2f} GB.")

print("-" * len(title))
print("")
