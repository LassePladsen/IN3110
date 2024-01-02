"""
Created on 01.10.2023
"""


import itertools  # ???

def fibonacci_gen(n_max):
    """Generates fibonacci numbers up to n_max iterations."""
    i = 0
    fpp = 1
    fp = 1
    while i < n_max:
        yield fpp
        fpp, fp = fp, fp+fpp
        i += 1
