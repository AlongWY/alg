import time
import numpy as np


def exe_time(func):
    def new_func(*args, **args2):
        t0 = time.time()
        back = func(*args, **args2)
        t1 = time.time()
        print("@%.3fs taken for {%s}" % (t1 - t0, func.__name__))
        return back, t1 - t0

    return new_func


def partition(array, p, r) -> int:
    i = np.random.randint(p, r)
    temp = array[i]
    array[i] = array[r]
    array[r] = temp

    x = array[r]
    i = p - 1
    for j in range(p, r):
        if array[j] < x:
            i = i + 1

            temp = array[i]
            array[i] = array[j]
            array[j] = temp

    temp = array[i + 1]
    array[i + 1] = array[r]
    array[r] = temp

    return i + 1


@exe_time
def quick_sort(array):
    def quick_sort_(array, p, r):
        if p < r:
            q = partition(array, p, r)
            quick_sort_(array, p, q - 1)
            quick_sort_(array, q + 1, r)

    return quick_sort_(array, 0, len(array) - 1)


sort = exe_time(np.sort)


def main():
    size = 1000000
    percents = list(range(10 + 1))
    np_ts = []
    ts = []
    for percent in percents:
        repeated = 1 - percent / 10
        source_array = np.random.randint(low=0, high=size * repeated + 1, size=size)
        sorted_array, np_t = sort(source_array)
        _, t = quick_sort(source_array)

        ts.append(t)
        np_ts.append(np_t)


if __name__ == '__main__':
    main()
