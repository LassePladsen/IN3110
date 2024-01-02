"""
Created on 01.10.2023
Ex2 week 4
"""

from time import time

def time_func(func):
    def wrapper(*args):
        t0 = time()
        output = func(*args)
        timing = time() - t0
        if not timing:  # rounded to zero:
            time_format = 0
        elif timing < 0.001 or timing > 1000:
            time_format = f"{timing:.3e}"
        else:
            time_format = f"{timing:.3f}"
        print(f"Function {func.__name__} executed in {time_format}s")
        return output

    return wrapper

cache_dir = {}
def cache(func):
    def wrapper(*args):
        # Check if already run this function with args
        if func in cache_dir.keys() and repr(args) in cache_dir[func]:  # if found return output to save time
            print("Found! getting output from cache")
            return cache_dir[func][repr(args)]
        else:  # not found, run func and cache
            print("Not found, running func and caching")
            output = func(*args)
            cache_dir[func] = {repr(args): output}
            return output
    return wrapper


@time_func
@cache
def my_func(*args):
    for i in range(int(10e7)):
        ...
    return args


if __name__ == "__main__":
    print(my_func(2, [1, 2]), "\n")
    print(my_func(2, [1, 2]), "\n")
    print(my_func("test"))
