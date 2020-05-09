# 凸包算法

from typing import List
from functools import cmp_to_key
from collections import namedtuple
from math import sqrt, acos, atan2
import numpy as np
import matplotlib.pyplot as plt


class Point(namedtuple('Point', ['x', 'y'])):
    def __repr__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(x=self.x + other.x, y=self.y + other.y)
        else:
            raise NotImplementedError()

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(x=self.x - other.x, y=self.y - other.y)
        else:
            raise NotImplementedError()

    def __mul__(self, other) -> float:
        # 点乘
        if isinstance(other, Point):
            return self.x * other.x + self.y * other.y
        else:
            raise NotImplementedError()

    def __matmul__(self, other):
        # 叉乘
        if isinstance(other, Point):
            return self.x * other.y - other.x * self.y
        else:
            raise NotImplementedError()

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __pos__(self):
        return self

    @property
    def angle(self):
        return atan2(self.y, self.x)


def point_in_triangle(a: Point, b: Point, c: Point, p: Point) -> bool:
    # p = A + u * (c - a) + v * (b - a)
    # u < 0 或者 v < 0 时，p 在外侧
    # u + v > 1, p 超出三角形
    v0 = c - a
    v1 = b - a
    v2 = p - a

    dot00 = v0 * v0
    dot01 = v0 * v1
    dot02 = v0 * v2
    dot11 = v1 * v1
    dot12 = v1 * v2

    try:
        inverDeno = 1.0 / (dot00 * dot11 - dot01 * dot01)
    except Exception:
        # 共线，等于不处理
        return False

    u = (dot11 * dot02 - dot01 * dot12) * inverDeno
    if u < 0 or u > 1:
        return False
    v = (dot00 * dot12 - dot01 * dot02) * inverDeno
    if v < 0 or v > 1:
        return False
    return u + v <= 1


@cmp_to_key
def cmp(a: Point, b: Point):
    if a.y < b.y:
        return -1
    elif a.y == b.y:
        return b.x - a.x
    else:
        return 1


def enum_closure(points: List[Point]):
    # 基于枚举的凸包求解算法
    if len(points) <= 3:
        return points

    points_num = len(points)
    points_use = [True] * points_num

    a = points[0]
    for i in range(1, points_num):
        if not points_use[i]:
            continue
        for j in range(i + 1, points_num):
            if not points_use[j]:
                continue
            for k in range(j + 1, points_num):
                if not points_use[k]:
                    continue
                b = points[i]
                c = points[j]
                d = points[k]
                if point_in_triangle(b, c, d, a):
                    points_use[0] = False
                if point_in_triangle(a, c, d, b):
                    points_use[i] = False
                if point_in_triangle(a, b, d, c):
                    points_use[j] = False
                if point_in_triangle(a, b, c, d):
                    points_use[k] = False

    points = sorted([point for use, point in zip(points_use, points) if use], key=cmp)
    points = points[:1] + sorted(points[1:], key=lambda x: (x - points[0]).angle)
    return points


def graham_sacn(points: List[Point]):
    # Graham扫描算法
    if len(points) <= 3:
        return points

    points = sorted(points, key=cmp)
    points = points[:1] + sorted(points[1:], key=lambda x: (x - points[0]).angle)

    i = 1
    while len(points) > 1:
        length = len(points)
        pi_pi1 = points[i % length] - points[(i - 1) % length]
        pi1_pi2 = points[(i + 1) % length] - points[i % length]

        if pi_pi1 @ pi1_pi2 <= 0:
            points.pop(i % length)
            i -= 1
            continue
        i += 1
        if i == len(points):
            break

    return points


def dc(points: List[Point]):
    # 基于分治的凸包求解算法
    if len(points) <= 3:
        points = sorted(points, key=cmp)
        points = points[:1] + sorted(points[1:], key=lambda x: (x - points[0]).angle)
        return points

    points = sorted(points, key=lambda x: x.x)
    middle = len(points) // 2

    left = dc(points[:middle])
    right = dc(points[middle:])

    left_size = len(left)
    right_size = len(right)

    left_most_right = left.index(max(left, key=lambda l: l.x))
    right_most_left = right.index(min(right, key=lambda r: r.x))

    # up support line
    left_up = left_most_right
    right_up = right_most_left
    while True:
        support_line = right[right_up] - left[left_up]

        right_forward = right[(right_up + 1) % right_size] - left[left_up]
        right_backword = right[(right_up - 1) % right_size] - left[left_up]

        if ((support_line @ right_forward) * (support_line @ right_backword)) < 0:
            right_up = (right_up - 1) % right_size
            continue

        left_forward = right[right_up] - left[(left_up + 1) % left_size]
        left_backword = right[right_up] - left[(left_up - 1) % left_size]

        if ((support_line @ left_forward) * (support_line @ left_backword)) < 0:
            left_up = (left_up + 1) % left_size
            continue
        break

    # down support line
    left_down = left_most_right
    right_down = right_most_left

    while True:
        support_line = left[left_down] - right[right_down]

        left_forward = left[(left_down + 1) % left_size] - right[right_down]
        left_backword = left[(left_down - 1) % left_size] - right[right_down]

        if ((support_line @ left_forward) * (support_line @ left_backword)) < 0:
            left_down = (left_down - 1) % left_size
            continue

        right_forward = left[left_down] - right[(right_down + 1) % right_size]
        right_backword = left[left_down] - right[(right_down - 1) % right_size]

        if ((support_line @ right_forward) * (support_line @ right_backword)) < 0:
            right_down = (right_down + 1) % right_size
            continue

        break

    res = []
    res.append(left[left_up])
    left_up = (left_up + 1) % left_size
    while left_up != left_down:
        res.append(left[left_up])
        left_up = (left_up + 1) % left_size

    res.append(right[right_down])
    right_down = (right_down + 1) % right_size
    while right_down != right_up:
        res.append(right[right_down])
        right_down = (right_down + 1) % right_size

    return res


def main():
    points_mat = np.random.randint(0, 101, size=(5, 2))
    points = [Point(x=x, y=y) for x, y in points_mat.tolist()]

    # enum_res = enum_closure(points)
    # x, y = zip(*enum_res)
    # plt.title('enum')
    # plt.scatter(points_mat[:, 0], points_mat[:, 1])
    # plt.plot(x, y)
    # plt.show()

    dc_res = dc(points)
    x, y = zip(*dc_res)
    plt.title('dc')
    plt.scatter(points_mat[:, 0], points_mat[:, 1])
    plt.plot(x, y)
    plt.show()

    graham_res = graham_sacn(points)
    x, y = zip(*graham_res)
    plt.title('graham_fix')
    plt.scatter(points_mat[:, 0], points_mat[:, 1])
    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    main()
