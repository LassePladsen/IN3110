# IN3110_INSTAPY

Apply filters to images using different implementations. Supports grayscale filter and sepia filter with implementations
of pure python, numpy, and numba. The command-line usage also supports image size scaling.

## Installation
Clone the repo

`git clone https://github.uio.no/IN3110/IN3110-lassepl.git`

Install it with pip from the root directory:

`pip3 install assignment3`

## Script usage
Import the different filters seperately in the following manner:
```python
from in3110_instapy.{implementation} import {implementation}_{filter}
```
where you replace `{implementation}` and `{filter}` with the desired implementation and filter as shown in the following table:

| Implementation | Description | | Filter        | Description      |
|----------------|-------------|-|---------------|------------------|
| `python`       | Pure python | | `color2gray`  | Grayscale filter |
| `numpy`        | Numby       | | `color2sepia` | Sepia filter     |
| `numba`        | Numba       | |               |                  |

Each of the filter functions have one argument, except `numpy.color2sepia` which has two. The first argument `image` is a 
`numpy.ndarray` containing image values in the shape `(H, W, C)` with `H, W` being the height and width of the image, 
and `C` being the three color channels red, green, and blue. For some `.png` images there may be a fourth channel 
representing transparency which also is supported. The second argument (only valid for `numpy.color2sepia`) `k` is the
sepia filter strength given as a float or integer in `[0, 1]`. `k=0` will return the original image and `k=1` will be 
the maximum sepia strength.

The intented way to use this package is using the ``Image`` module from the `Pillow`/`PIL` package to open images and 
convert them to `numpy.ndarray` using `numpy.asarray(image)`.

### Script example
Applying sepia filter using the numpy implementation with sepia strength `k=0.7`:
```python
from PIL import Image
import numpy as np
from in3110_instapy.numpy_filters import numpy_color2sepia

# Load an image
file = "test.png"
image = Image.open(file)

# Load image into array
image_array = np.asarray(image)

# Apply filter
filtered_image_array = numpy_color2sepia(
        image_array,
        k=0.7)

# Convert back to Image
filtered_image = Image.fromarray(filtered_image_array)

# Display image
filtered_image.show()

# Save image
outfile = "test_filtered.png"
filtered_image.save(outfile)
```

## Command-line usage
```
usage: in3110_instapy [-h] [-o OUT] (-g | -se) [-sc SCALE] [-i {python,numpy,numba}] [-st STRENGTH] [-r] file

Apply filters to images.

positional arguments:
  file                  The filename to apply filter to

options:
  -h, --help            show this help message and exit
  -o OUT, --out OUT     The output filename, if missing only displays filtered image without saving
  -g, --gray            Select gray filter
  -se, --sepia          Select sepia filter
  -sc SCALE, --scale SCALE
                        Scale factor to resize image
  -i {python,numpy,numba}, --implementation {python,numpy,numba}
                        Select filter implementation, defaults to 'numba'
  -st STRENGTH, --strength STRENGTH
                        Filter strength, only valid for numpy.color2sepia implementation
  -r, --runtime         Track average runtime over 3 runs of chosen task
```

### Command-line example
Using the pure python implementation of the grayscale filter and scaling the image down to half size, 
and saving the result:

```
python3 -m in3110_instapy "test.jpg" --out "test_filtered.jpg" --gray --scale 0.5
```
and the above is equivalent to
```
python3 -m in3110_instapy "test.jpg" -o "test_filtered.jpg" -g -sc 0.5
```

