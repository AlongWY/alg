import time
import numpy as np
import matplotlib.pyplot as plt
from quicksort import cppsort, quicksort, quicksort_opt


def exe_time(func):
    def new_func(*args, **args2):
        t0 = time.time()
        back = func(*args, **args2)
        t1 = time.time()
        print("@%.3fs taken for {%s}" % (t1 - t0, func.__name__))
        return back, t1 - t0

    return new_func


cppsort = exe_time(cppsort)
quicksort = exe_time(quicksort)
quicksort_opt = exe_time(quicksort_opt)


def main():
    size = 1000000
    percents = list(range(10 + 1))
    cpp_ts = []
    ext_ts = []
    opt_ts = []
    for percent in percents:
        print(percent)
        repeated = 1 - percent / 10
        source_array = np.random.randint(low=0, high=size * repeated + 1, size=size)
        sorted_array, cpp_t = cppsort(source_array)
        sorted_array_opt, opt_t = quicksort_opt(source_array)
        cpp_ts.append(cpp_t)
        opt_ts.append(opt_t)

        if percent < 10:
            sorted_array_ext, ext_t = quicksort(source_array)
            ext_ts.append(ext_t)
        else:
            ext_ts.append(ext_ts[-1] * 1.1)

    plt.plot(percents, cpp_ts)
    plt.plot(percents, ext_ts)
    plt.plot(percents, opt_ts)
    plt.show()


if __name__ == '__main__':
    main()
