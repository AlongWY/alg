import time, random
import matplotlib.pyplot as plt


def exe_time(func):
    def new_func(*args, **args2):
        t0 = time.time()
        back = func(*args, **args2)
        t1 = time.time()
        print("@%.3fs taken for {%s}" % (t1 - t0, func.__name__))
        return back, t1 - t0

    return new_func


@exe_time
def greedy(X: set, F: list):
    price = {x: 1 for x in X}
    U = set()
    C = []
    while U != X:
        s_u = None
        min_s = None
        min_cost = float("inf")
        for i, s in enumerate(F):
            temp = s - U
            cost = (1 / len(temp)) if len(temp) > 0 else float("inf")
            if cost < min_cost:
                min_s = i
                s_u = temp
                min_cost = cost

        for e in s_u:
            price[e] = min_cost

        U.update(s_u)
        C.append(F.pop(min_s))

    return C


@exe_time
def linear(X: set, F: list):
    from itertools import chain
    from collections import Counter
    from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value
    problem = LpProblem(sense=LpMinimize)
    variables = [LpVariable(f"x{i}", 0) for i in range(len(F))]

    # 最小化函数
    problem += lpSum(variables)

    # 约束，X中的元素都至少有一个
    for e in X:
        problem += (lpSum([xs for idx, xs in enumerate(variables) if e in F[idx]]) >= 1)

    problem.solve()

    f = 1. / Counter(chain(*F)).most_common(1)[0][1]
    return [F[index] for index, var in enumerate(variables) if value(var) >= f]


def generate(size: int):
    x_set_source = set(range(size))
    x_set = x_set_source
    res = [set(random.sample(x_set, 20))]
    x_set = x_set.difference(res[-1])
    while len(x_set) > 20:
        n = random.randint(1, 20)
        x = random.randint(1, n)
        s = random.sample(x_set, n - x)
        s.extend(random.sample(x_set, x))
        res.append(set(s))
        x_set = x_set.difference(res[-1])

    res.append(x_set)

    for i in range(size - len(res)):
        n = random.randint(1, 20)
        res.append(set(random.sample(x_set_source, n)))

    return x_set_source, res


def check(X, S):
    union = set()
    for s in S:
        union.update(s)

    return union == X


def main():
    sizes = [50, 100, 500, 1000, 2000, 4000, 5000]
    linear_sizes = []
    greedy_sizes = []

    linear_times = []
    greedy_times = []
    for size in sizes:
        X, F = generate(size)
        res, greedy_time = greedy(X, F)
        greedy_sizes.append(len(res))
        res, linear_time = linear(X, F)
        linear_sizes.append(len(res))

        linear_times.append(linear_time)
        greedy_times.append(greedy_time)

    plt.plot(sizes, greedy_sizes, color='g', label="greedy")
    plt.plot(sizes, linear_sizes, color='r', label="linear")
    plt.legend()
    plt.savefig("approximate_size")
    plt.show()

    plt.plot(sizes, greedy_times, color='g', label="greedy")
    plt.plot(sizes, linear_times, color='r', label="linear")
    plt.legend()
    plt.savefig("approximate")
    plt.show()


if __name__ == '__main__':
    main()
