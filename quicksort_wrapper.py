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
    threshold = 7
    for percent in percents:
        repeated_ratio = 1 - percent / 10
        not_repeated = list(range(1, int(size * repeated_ratio)))
        if len(not_repeated) > 0:
            repeated = [random.choice(not_repeated)] * (size - len(not_repeated))
        else:
            repeated = [0] * size
        source_array = repeated + not_repeated
        random.shuffle(source_array)

        c_sorted_array, c_t = csort(source_array)
        cpp_sorted_array, cpp_t = cppsort(source_array)
        opt_sorted_array, opt_t = quicksort_opt(source_array)

        assert cpp_sorted_array == opt_sorted_array

        c_ts.append(c_t)
        cpp_ts.append(cpp_t)
        opt_ts.append(opt_t)

        if percent < threshold:
            ext_sorted_array, ext_t = quicksort(source_array)
            assert cpp_sorted_array == opt_sorted_array
            ext_ts.append(ext_t)

    plt.plot(percents[:threshold], ext_ts, label='quicksort')
    plt.savefig("quicksort")
    plt.show()

    plt.plot(percents, c_ts, label='c')
    plt.plot(percents, cpp_ts, label='c++')
    plt.plot(percents, opt_ts, label='opt')
    plt.legend()
    plt.savefig("quicksort_opt")
    plt.show()


if __name__ == '__main__':
    main()
