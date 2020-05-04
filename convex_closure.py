# 凸包算法

from typing import List
from collections import namedtuple
from math import sqrt


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
        if isinstance(other, Point):
            return self.x * other.x + self.y * other.y
        else:
            raise NotImplementedError()


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


def enum_closure(points: List[Point]):
    # 基于枚举的凸包求解算法
    if len(points) <= 3:
        return points

    points_num = len(points)
    points_use = [True] * points_num
    for i in range(points_num):
        for j in range(i + 1, points_num):
            for k in range(j + 1, points_num):
                for p in range(k + 1, points_num):
                    a = points[i]
                    b = points[j]
                    c = points[k]
                    d = points[p]
                    if point_in_triangle(b, c, d, a):
                        points_use[i] = False
                    if point_in_triangle(a, c, d, b):
                        points_use[j] = False
                    if point_in_triangle(a, b, d, c):
                        points_use[k] = False
                    if point_in_triangle(a, b, c, d):
                        points_use[p] = False

    return [point for use, point in zip(points_use, points) if use]


def graham_sacn(points: List[Point]):
    # Graham扫描算法
    pass


def dc(points: List[Point]):
    # 基于分治的凸包求解算法
    pass


if __name__ == '__main__':
    a = Point(x=0, y=0)
    b = Point(x=1, y=0)
    c = Point(x=0, y=1)
    d = Point(x=1, y=1)
    e = Point(x=-1, y=-1)

    print(enum_closure([a, b, c, d, e]))
