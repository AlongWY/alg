import time
import numpy as np
import matplotlib.pyplot as plt
from quicksort import csort, cppsort, quicksort, quicksort_opt


def exe_time(func):
    def new_func(*args, **args2):
        t0 = time.time()
        back = func(*args, **args2)
        t1 = time.time()
        print("@%.3fs taken for {%s}" % (t1 - t0, func.__name__))
        return back, t1 - t0

    return new_func


csort = exe_time(csort)
cppsort = exe_time(cppsort)
quicksort = exe_time(quicksort)
quicksort_opt = exe_time(quicksort_opt)


def main():
    size = 1000000
    percents = list(range(10 + 1))
    c_ts = []
    cpp_ts = []
    ext_ts = []
    opt_ts = []
    for percent in percents:
        print(percent)
        repeated = 1 - percent / 10
        source_array = np.random.randint(low=0, high=size * repeated + 1, size=size)
        sorted_array, c_t = csort(source_array)
        sorted_array, cpp_t = cppsort(source_array)
        sorted_array, opt_t = quicksort_opt(source_array)

        c_ts.append(c_t)
        cpp_ts.append(cpp_t)
        opt_ts.append(opt_t)

        if percent < 10:
            sorted_array, ext_t = quicksort(source_array)
            ext_ts.append(ext_t)

    plt.plot(percents, c_ts)
    plt.plot(percents, cpp_ts)
    plt.plot(percents, opt_ts)
    plt.show()
    plt.plot(percents[:10], ext_ts)
    plt.show()


if __name__ == '__main__':
    main()
