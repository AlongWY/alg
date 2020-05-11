# 凸包算法
import time
from typing import List
from functools import cmp_to_key
from collections import namedtuple
from math import sqrt, atan2
import numpy as np
import matplotlib.pyplot as plt


def exe_time(func):
    def new_func(*args, **args2):
        t0 = time.time()
        back = func(*args, **args2)
        t1 = time.time()
        print("@%.3fs taken for {%s}" % (t1 - t0, func.__name__))
        return back, t1 - t0

    return new_func


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
        return a.x - b.x
    else:
        return 1


@exe_time
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


@exe_time
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


def relative(a, b, c):
    # a --> b
    return (a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x)


@cmp_to_key
def x_cmp(a: Point, b: Point):
    if a.x < b.x:
        return -1
    elif a.x == b.x:
        return a.y - b.y
    else:
        return 1


@exe_time
def dc(points: List[Point]):
    def dc_(points: List[Point]):
        # 基于分治的凸包求解算法
        if len(points) <= 3:
            points = sorted(points, key=cmp)
            return points[:1] + sorted(points[1:], key=lambda x: (x - points[0]).angle)

        middle = points[len(points) // 2].x

        left = [point for point in points if point.x < middle]
        right = points[len(left):]
        left = dc_(left)
        if len(left) == len(points):
            return left
        right = dc_(right)

        left_size = len(left)
        right_size = len(right)

        left_most_right = left.index(max(left, key=lambda l: l.x))
        right_most_left = right.index(min(right, key=lambda r: r.x))

        # up support line
        left_up = left_most_right
        right_up = right_most_left
        while True:
            right_forward = right[(right_up + 1) % right_size]
            right_backword = right[(right_up - 1) % right_size]
            if not (len(right) == 1 or (relative(left[left_up], right[right_up], right_forward) <= 0
                                        and relative(left[left_up], right[right_up], right_backword) <= 0)):
                right_up = (right_up - 1) % right_size
                continue

            left_forward = left[(left_up + 1) % left_size]
            left_backword = left[(left_up - 1) % left_size]
            if not (len(left) == 1 or (relative(left[left_up], right[right_up], left_forward) <= 0 and
                                       relative(left[left_up], right[right_up], left_backword) <= 0)):
                left_up = (left_up + 1) % left_size
                continue
            break

        # down support line
        left_down = left_most_right
        right_down = right_most_left

        while True:
            left_forward = left[(left_down + 1) % left_size]
            left_backword = left[(left_down - 1) % left_size]
            if not (len(left) == 1 or (relative(left[left_down], right[right_down], left_forward) >= 0 and
                                       relative(left[left_down], right[right_down], left_backword) >= 0)):
                left_down = (left_down - 1) % left_size
                continue

            right_forward = right[(right_down + 1) % right_size]
            right_backword = right[(right_down - 1) % right_size]
            if not (len(right) == 1 or (relative(left[left_down], right[right_down], right_forward) >= 0
                                        and relative(left[left_down], right[right_down], right_backword) >= 0)):
                right_down = (right_down + 1) % right_size
                continue
            break

        points = []
        for i in range(left_up, left_up + left_size):
            points.append(left[i % left_size])
            if i % left_size == left_down:
                break
        for i in range(right_down, right_down + right_size):
            points.append(right[i % right_size])
            if i % right_size == right_up:
                break
        return points

    return dc_(points)


def filter_points(points):
    points = sorted(points, key=x_cmp)
    filter_points = [points.pop(0)]
    last_equal = None
    while len(points):
        point = points.pop(0)
        if point.x != filter_points[-1].x:
            if last_equal:
                filter_points.append(last_equal)
                last_equal = None
            filter_points.append(point)
            continue
        last_equal = point
    if last_equal and last_equal.y != filter_points[-1].y:
        filter_points.append(last_equal)
    return filter_points


def display(title, line, points_mat):
    x, y = zip(*line)
    plt.title(title)
    plt.scatter(points_mat[:, 0], points_mat[:, 1])
    plt.scatter(x, y, color='r')
    plt.plot(x, y, color='r')
    plt.show()


def test():
    points_mat = 100 * np.random.rand(1000, 2)
    points = [Point(x=x, y=y) for x, y in points_mat.tolist()]
    points = filter_points(points)

    enum_res, enum_t_1000 = enum_closure(points)
    dc_res, dc_t_1000 = dc(points)
    graham_res, graham_t_1000 = graham_sacn(points)

    display('enum', enum_res, points_mat)
    display('dc', dc_res, points_mat)
    display('graham', graham_res, points_mat)


def main():
    sizes = [10, 50, 100, 500, 1000, 1500, 2000, 2500, 3000]
    enum_ts = []
    dc_ts = []
    graham_ts = []

    for size in sizes:
        points_mat = 100 * np.random.rand(size, 2)
        points = [Point(x=x, y=y) for x, y in points_mat.tolist()]
        points = filter_points(points)

        enum_res, enum_t = enum_closure(points)
        dc_res, dc_t = dc(points)
        graham_res, graham_t = graham_sacn(points)

        enum_ts.append(enum_t)
        dc_ts.append(dc_t)
        graham_ts.append(graham_t)

    plt.title("enum")
    plt.plot(sizes, enum_ts, color='r')
    plt.show()
    plt.title("dc")
    plt.plot(sizes, dc_ts, color='g')
    plt.show()
    plt.title("graham")
    plt.plot(sizes, graham_ts, color='b')
    plt.show()


if __name__ == '__main__':
    test()
    main()
