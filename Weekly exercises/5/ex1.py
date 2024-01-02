"""
Created on 01.10.2023
"""

import numpy as np
from numba import jit
from timeit import timeit

@jit(nopython=True)
def arange_2d(arr):
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            arr[i, j] = i * j

N = 10_000
arr = np.empty((N, N))

print(timeit(lambda: arange_2d(arr), number=30))
