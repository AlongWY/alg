cdef extern from "math.h":
    double sqrt(double theta)
    double atan2(double y, double x)

cdef class Point:
    cdef public double x, y, angle
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = atan2(self.y, self.x)

    def __repr__(self)-> str:
        return f"({self.x},{self.y})"

    def __eq__(self, other: Point)-> bool:
        # cdef Point other
        return self.x == other.x and self.y == other.y

    def __abs__(self) -> double:
        return sqrt(self.x * self.x + self.y * self.y)

    def __add__(self, other: Point) -> Point:
        # cdef Point other
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point)-> Point:
        # cdef Point other
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Point) -> double:
        # 点乘
        return self.x * other.x + self.y * other.y

    def __matmul__(self, other: Point) -> double:
        # 叉乘
        return self.x * other.y - other.x * self.y

    def __neg__(self) -> Point:
        return Point(-self.x, -self.y)

    def __pos__(self) -> Point:
        return self

cpdef bint point_in_triangle(a: Point, b: Point, c: Point, p: Point):
    cdef Point v0, v1, v2
    cdef double dot00, dot01, dot02, dot11, dot12
    cdef double inverDeno, u, v
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
        return 0

    u = (dot11 * dot02 - dot01 * dot12) * inverDeno
    if u < 0. or u > 1.:
        return 0
    v = (dot00 * dot12 - dot01 * dot02) * inverDeno
    if v < 0. or v > 1.:
        return 0
    return u + v <= 1.

cpdef double relative(a: Point, b: Point, c: Point):
    # cdef Point a, b, c
    # a --> b
    return (a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x)

cpdef double cmp(a: Point, b: Point):
    # cdef Point a, b
    if a.y < b.y:
        return -1.0
    elif a.y == b.y:
        return a.x - b.x
    else:
        return 1.0

cpdef double x_cmp(a: Point, b: Point):
    # cdef Point a, b, c
    if a.x < b.x:
        return -1.0
    elif a.x == b.x:
        return a.y - b.y
    else:
        return 1.0
