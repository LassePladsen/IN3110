"""numpy implementation of image filters"""
from __future__ import annotations

import numpy as np


def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """

    # Weighted sum with weights (r,g,b) = (0.21, 0.72, 0.07)
    weights = np.asarray([0.21, 0.72, 0.07])
    gray_image = np.dot(image[:, :, :3], weights)

    # Duplicate the weighted sum to three uniform rgb-channel values
    gray_image = np.stack((gray_image,) * 3, axis=-1)

    gray_image = gray_image.astype("uint8")  # Convert to unsigned 8 bit ints
    return gray_image


def numpy_color2sepia(image: np.array, k: float = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    (note: implementing 'k' is a bonus task,
        you may ignore it)

    Returns:
        np.array: sepia_image
    """

    if not 0 <= k <= 1:
        raise ValueError(f"k must be in [0-1], got {k=}")

    # Create sepia weights
    sepia_matrix = np.asarray([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131],
    ])

    # Apply the sepia filter
    sepia_image = np.dot(image[:, :, :3], sepia_matrix.T)  # 3 first channels (rgb) if more than 3

    # Check for overflow with uint8
    max_value = np.max(sepia_image)
    if max_value > 255:  # overflow with uint8, scale all down from max value
        scale = 255 / max_value
        sepia_image *= scale

    # Implement sepia scaling variable k:
    sepia_image = k * sepia_image + (1 - k) * image[:, :, :3]

    # Convert back into uint8
    return sepia_image.astype("uint8")
