"""
Created on 15.09.2023
Exercise 4: https://pages.github.uio.no/IN3110/assignments/exercises/week4.html#exercise-1-blurring-images
"""

from pathlib import Path

import numpy as np
from PIL import Image


def blur_image(image_path: str | Path, output_path: str | Path = "") -> None:
    """Blurs the given image file and saves it to the given output path.

    Parameters:
        - image_path (str or pathlib.Path) : input image filepath.
        - output_path (str or pathlib.Path) : output image filepath to be saved. Defaults to current working directory
            with filename inherited from the input filename.

    Returns:
        None
    """

    # Convert to Path to catch wrong input types with better error msg than PIL.Image
    image_path = Path(image_path)

    # Check if exists and is file (PIL.Image will do this, but this is for a custom error msg. 
    if not image_path.is_file():
        raise FileNotFoundError(f"Given input image path 'image_path' must be an existing file ('{str(image_path)}').")

    # Create default image output path
    if not output_path:
        output_path = (str(image_path)[:str(image_path).index(".")] + "_blurred"
                       + str(image_path)[str(image_path).index("."):])

    # Open image
    img = np.asarray(Image.open(image_path), dtype=np.int32)
    blurred = np.zeros_like(img, dtype=np.int32)

    # Pad image array with 1 pixel at top, bottom, left, and right for the blur logic
    img = np.pad(img, 1, mode="edge")

    # Blur the image by averaging the images [H,W,C]-values (this is the img array's shape) with its neighbours' values.
    for h in range(blurred.shape[0]):  # height-values
        for w in range(blurred.shape[1]):  # width-values
            # only do the rgb-values, not transparency value which should be the fourth index in the following line:
            for c in range(3):  # channel-values (rgb-transparency)
                blurred[h, w, c] = (img[h, w, c] + img[h - 1, w, c] + img[h + 1, w, c]
                                    + img[h, w - 1, c] + img[h, w + 1, c]
                                    + img[h - 1, w - 1, c] + img[h - 1, w + 1, c]
                                    + img[h + 1, w - 1, c] + img[h + 1, w + 1, c]) / 9

    # Convert to integers
    blurred = blurred.astype("uint8")

    # Save blurred image
    Image.fromarray(blurred).save(output_path)


if __name__ == "__main__":
    # if len(argv) < 2:
    #     print("Please provide a input image filepath:")
    #     image = input("$ ")
    #     outpath = ""
    # elif len(argv) == 3:
    #     image = argv[1]
    #     outpath = ""
    # elif len(argv) > 3:
    #     image = argv[1]
    #     outpath = argv[2]
    image = "test.png"
    outpath = ""
    blur_image(image, outpath)

    # TODO: THIS SHIT DONT FUCKING WORK!???
