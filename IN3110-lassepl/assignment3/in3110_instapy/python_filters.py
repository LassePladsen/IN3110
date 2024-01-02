"""pure Python implementation of image filters"""
from __future__ import annotations

import numpy as np


def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale.

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """

    gray_image = np.empty_like(image)

    # iterate through the pixels, and apply the grayscale transform
    for h in range(gray_image.shape[0]):  # height-values
        for w in range(gray_image.shape[1]):  # width-values
            # Weighted sum with weights (r,g,b) = (0.21, 0.72, 0.07)
            gray_image[h, w, :] = 0.21 * image[h, w, 0] + 0.72 * image[h, w, 1] + 0.07 * image[h, w, 2]

    gray_image = gray_image.astype("uint8")  # convert back into unsigned 8 bit ints
    return gray_image


def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """

    sepia_image = np.empty_like(image).astype(np.float32)

    sepia_matrix = [
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131],
    ]

    # Iterate through the pixels, applying the sepia matrix conversion
    current_max = 0
    for h in range(sepia_image.shape[0]):  # height-values
        for w in range(sepia_image.shape[1]):  # width-values
            r, g, b = image[h, w]

            # Take average of all rbg-values and multiply with weights in sepia_matrix
            sepia_r = r * sepia_matrix[0][0] + g * sepia_matrix[0][1] + b * sepia_matrix[0][2]
            sepia_g = r * sepia_matrix[1][0] + g * sepia_matrix[1][1] + b * sepia_matrix[1][2]
            sepia_b = r * sepia_matrix[2][0] + g * sepia_matrix[2][1] + b * sepia_matrix[2][2]

            # Create new sepia image values
            sepia_image[h, w] = np.asarray([sepia_r, sepia_g, sepia_b])

            # Save maximum found value for later scaling
            new_max = max(sepia_r, sepia_g, sepia_b)
            if new_max > current_max:
                current_max = new_max

    # Then check for uint8 overflow (>255)
    if current_max > 255:
        # Then scale all values for uint8 overflow (over 255) with the max value with new loop
        scale = 255 / current_max
        for h in range(sepia_image.shape[0]):  # height-values
            for w in range(sepia_image.shape[1]):  # width-values
                for c in range(3):  # rbg-channels
                    sepia_image[h, w, c] = sepia_image[h, w, c] * scale

    # Convert back to unsigned 8 bit ints
    return sepia_image.astype("uint8")
