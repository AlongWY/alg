def greedy(X: set, F: list):
    U = X
    C = []
    while len(U):
        max_f = None
        max_common = 0
        for i, f in enumerate(F):
            common = len(f & U)
            if common > max_common:
                max_f = i
                max_common = common
        U = U - F[max_f]
        C.append(F[max_f])
        F.pop(max_f)

    return C


def main():
    X = set([1, 2, 3, 4, 5, 6, 7])
    F = [set([1, 2, 3, 4]), set([2, 3, 4]), set([5, 6, 7])]
    print(greedy(X, F))


if __name__ == '__main__':
    main()
