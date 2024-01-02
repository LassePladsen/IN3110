from __future__ import annotations

from timeit import timeit
import numpy as np
from PIL import Image
from typing import Callable

from . import get_filter, io


def time_one(filter_function: Callable, *arguments, calls: int = 3) -> float:
    """Return the time for one call

    When measuring, repeat the call `calls` times,
    and return the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """
    filter_function(*arguments)  # Call function once before measurement for numba jit compiling
    return timeit(lambda: filter_function(*arguments), number=calls)


def make_reports(filename: str = "test/rain.jpg", calls: int = 3) -> None:
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Prints and saves the result to "timing-report.txt" in the working dir.

    Args:
        filename (str): the image file to use
        calls (int): amount of calls to

    Returns:
        None
    """

    # load the image
    image = Image.open(filename)

    # Write report to an outfile
    with open("timing-report.txt", "w") as outfile:
        # Print the image name and dimensions
        w, h = image.size
        outfile.write(f"Timing performed using {filename}: {w}x{h}\n\n")

        # Get image array
        image = np.asarray(image)

        # iterate through the filters
        filter_names = [
            "color2gray",
            "color2sepia"
        ]

        for filter_name in filter_names:
            # get the reference filter function
            reference_filter = get_filter(filter_name, "python")

            # time the reference implementation
            reference_time = time_one(reference_filter, image, calls=calls)

            outfile.write(
                f"Reference (pure Python) filter time {filter_name}: {reference_time:.3}s ({calls=})\n"
            )

            # iterate through the implementations
            implementations = [
                "numpy",
                "numba"
            ]

            for implementation in implementations:
                filter = get_filter(filter_name, implementation)

                # time the filter
                filter_time = time_one(filter, image, calls=calls)

                # compare the reference time to the optimized time
                speedup = reference_time / filter_time

                outfile.write(
                    f"Timing: {implementation} {filter_name}: {filter_time:.3}s ({speedup=:.2f}x)\n"
                )
            outfile.write("\n")  # new line between filters


if __name__ == "__main__":
    # run as `python -m in3110_instapy.timing`
    make_reports()
