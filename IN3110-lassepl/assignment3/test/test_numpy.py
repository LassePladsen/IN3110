import numpy as np
from in3110_instapy.numpy_filters import numpy_color2gray, numpy_color2sepia


def test_color2gray(image):
    filter_image = numpy_color2gray(image)

    # check that the result has the right shape, type
    assert filter_image.shape == image.shape
    assert filter_image.dtype == "uint8"

    # Check a few pixels
    for pixel in [2, 8, 15]:
        # Assert uniform pixel values
        assert filter_image[pixel, pixel].sum() / 3 == filter_image[pixel, pixel, 0]

        # Assert the pixels have weighted sum with weights (r,g,b) = (0.21, 0.72, 0.07)
        weights = np.asarray([0.21, 0.72, 0.07])
        expected = np.dot(image[pixel, pixel], weights)
        actual = filter_image[pixel, pixel, 0]
        np.testing.assert_allclose(actual, expected, rtol=0.05)  # within 5%


def test_color2sepia(image):
    for k in [0, 0.23, 0.6, 1]:  # test for four k-values
        filter_image = numpy_color2sepia(image, k)

        # check that the result has the right shape, type
        assert filter_image.shape == image.shape
        assert filter_image.dtype == "uint8"

        sepia_matrix = np.asarray([
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131],
        ])

        # verify a few pixel samples are correct according to the sepia matrix within a tolerance
        for pixel in [6, 8, 15]:
            expected = k * np.dot(image[pixel, pixel], sepia_matrix.T) + (1 - k) * image[pixel, pixel]
            actual = k * filter_image[pixel, pixel] + (1 - k) * image[pixel, pixel]
            np.testing.assert_allclose(actual, expected,
                                       rtol=0.2,  # Because of the scaling down to avoid overflow I add an absolute
                                       atol=50)  # tolerance here
