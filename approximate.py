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
    return [F[index] for index, var in enumerate(variables) if value(var) > f]


def main():
    X = {1, 2, 3, 4, 5, 6, 7}
    F = [{1, 2, 3, 4}, {2, 3, 4}, {4, 5, 6, 7}]
    print(linear(X, F))
    print(greedy(X, F))


if __name__ == '__main__':
    main()
