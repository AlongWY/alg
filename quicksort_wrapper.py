import time
import random
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
        repeated_ratio = 1 - percent / 10
        not_repeated = list(range(1, int(size * repeated_ratio)))
        repeated = [0] * (size - len(not_repeated))
        source_array = repeated + not_repeated
        random.shuffle(source_array)

        c_sorted_array, c_t = csort(source_array)
        cpp_sorted_array, cpp_t = cppsort(source_array)
        opt_sorted_array, opt_t = quicksort_opt(source_array)

        assert cpp_sorted_array == opt_sorted_array

        c_ts.append(c_t)
        cpp_ts.append(cpp_t)
        opt_ts.append(opt_t)

        if percent < 7:
            ext_sorted_array, ext_t = quicksort(source_array)
            assert cpp_sorted_array == opt_sorted_array
            ext_ts.append(ext_t)

    plt.plot(percents, c_ts)
    plt.plot(percents, cpp_ts)
    plt.plot(percents, opt_ts)
    plt.show()
    plt.plot(percents[:10], ext_ts)
    plt.show()


if __name__ == '__main__':
    main()
