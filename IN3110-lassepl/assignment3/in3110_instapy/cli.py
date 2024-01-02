"""Command-line (script) interface to instapy"""
from __future__ import annotations

import argparse
import sys
import time

import in3110_instapy
import numpy as np
from PIL import Image


def check_positive_number(num: int | float | str):
    """Raises an argparse.ArgumentTypeError if the given number is negative,
     returns the number if it is positive."""
    num = float(num)
    if num < 0:
        raise argparse.ArgumentTypeError(f"Argument must be a non-negative number, got '{num}'")
    return num


def run_filter(
        file: str,
        out_file: str = None,
        implementation: str = "python",
        filter: str = "color2gray",
        scale: int = 1,
        strength: int = 1,
        n_runs: int = 1
) -> None:
    """Run the selected filter"""

    if n_runs < 1:  # number of runs must be greater than zero
        raise ValueError(f"Number of runs must be greater than zero, got: '{n_runs=}'.")

    for i in range(n_runs):
        # load the image from a file
        image = Image.open(file)

        # Resize image, if needed
        if scale != 1:
            w, h = image.size
            new_size = int(scale * w), int(scale * h)
            image = image.resize(new_size)

        image = np.asarray(image)

        # Apply the filter
        if filter == "color2sepia" and implementation == "numpy":
            filtered = in3110_instapy.get_filter(filter, implementation)(image, strength)
        else:
            filtered = in3110_instapy.get_filter(filter, implementation)(image)

    if out_file:
        Image.fromarray(filtered).save(out_file)

    else:  # not asked to save, display it instead
        Image.fromarray(filtered).show()


def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
            prog="in3110_instapy",
            description="Apply filters to images.")

    # Positional argument: filename
    parser.add_argument(
            "file",
            help="The filename to apply filter to")

    # Optional output filename arguments:
    parser.add_argument(
            "-o", "--out",
            help="The output filename, if missing only displays filtered image without saving")

    # Require either -g or -se filter options:
    filter_group = parser.add_mutually_exclusive_group(required=True)
    filter_group.add_argument(
            "-g", "--gray",
            help="Select gray filter",
            action="store_true")
    filter_group.add_argument(
            "-se", "--sepia",
            help="Select sepia filter",
            action="store_true")

    # Other optional options:
    parser.add_argument(
            "-sc", "--scale",
            help="Scale factor to resize image",
            default=1,
            type=check_positive_number)
    parser.add_argument(
            "-i", "--implementation",
            help="Select filter implementation, defaults to 'numba'",
            choices=["python", "numpy", "numba"],
            default="numba")
    parser.add_argument(
            "-st", "--strength",
            help="Filter strength, only valid for numpy.color2sepia implementation",
            default=1,
            type=check_positive_number
    )
    n_runs = 3
    parser.add_argument(
            "-r", "--runtime",
            help=f"Track average runtime over {n_runs} runs of chosen task",
            action="store_true"
    )

    # parse arguments and call run_filter()
    args = parser.parse_args(argv)

    if args.gray:
        filter_ = "color2gray"
    else:
        filter_ = "color2sepia"

    if args.runtime:  # --runtime flag: do 3 runs and print average runtime to stdout
        start_time = time.time()
        run_filter(
                file=args.file,
                out_file=args.out,
                filter=filter_,
                scale=args.scale,
                implementation=args.implementation,
                strength=args.strength,
                n_runs=n_runs
        )
        end_time = time.time()
        mean_time = (end_time - start_time) / n_runs
        print(f"Average time over {n_runs} runs: {mean_time:.3f}s")

    else:
        run_filter(
                file=args.file,
                out_file=args.out,
                filter=filter_,
                scale=args.scale,
                implementation=args.implementation,
                strength=args.strength,
                n_runs=1
        )
