import numpy as np
from in3110_instapy.python_filters import python_color2gray, python_color2sepia


def test_color2gray(image):
    filter_image = python_color2gray(image)

    # check that the result has the right shape, type
    assert filter_image.shape == image.shape
    assert filter_image.dtype == "uint8"

    # Check a few pixels
    for pixel in [0, 5, 10]:
        # Assert uniform pixel values
        assert filter_image[pixel, pixel].sum() / 3 == filter_image[pixel, pixel, 0]

        # Assert the pixels have weighted sum with weights (r,g,b) = (0.21, 0.72, 0.07)
        weights = np.asarray([0.21, 0.72, 0.07])
        expected = np.dot(image[pixel, pixel], weights)
        actual = filter_image[pixel, pixel, 0]
        np.testing.assert_allclose(expected, actual, rtol=0.05)  # within 5%


def test_color2sepia(image):
    filter_image = python_color2sepia(image)

    # check that the result has the right shape, type
    assert filter_image.shape == image.shape
    assert filter_image.dtype == "uint8"

    sepia_matrix = [
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131],
    ]

    # verify a few pixel samples are correct according to the sepia matrix within a tolerance
    for pixel in [0, 8, 15]:
        r, g, b = image[pixel, pixel]
        rs, gs, bs = filter_image[pixel, pixel]
        expected = [
            r * sepia_matrix[0][0] + g * sepia_matrix[0][1] + b * sepia_matrix[0][2],
            r * sepia_matrix[1][0] + g * sepia_matrix[1][1] + b * sepia_matrix[1][2],
            r * sepia_matrix[2][0] + g * sepia_matrix[2][1] + b * sepia_matrix[2][2]
        ]
        actual = [
            rs * sepia_matrix[0][0] + gs * sepia_matrix[0][1] + bs * sepia_matrix[0][2],
            rs * sepia_matrix[1][0] + gs * sepia_matrix[1][1] + bs * sepia_matrix[1][2],
            rs * sepia_matrix[2][0] + gs * sepia_matrix[2][1] + bs * sepia_matrix[2][2]
        ]
        np.testing.assert_allclose(actual, expected, rtol=0.15)  # Within 15%
