from math import sqrt
from collections import namedtuple
from queue import PriorityQueue

Point = namedtuple('Point', ['x', 'y'])


class Position(object):
    def __init__(self, x, y, g, h, parent=None):
        self.x = x
        self.y = y
        self.g = g  # start -> current
        self.h = h  # current -> end
        self.parent = parent

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(x=self.x + other.x, y=self.y + other.y)
        else:
            raise NotImplementedError()

    def __lt__(self, other):
        if isinstance(other, Position):
            return (self.g + self.h) < (other.g + other.h)
        else:
            raise NotImplementedError()

    def __hash__(self):
        return hash(f"{self.x},{self.y}")

    def __repr__(self):
        return f"({self.x},{self.y},f={self.g})"

    def __eq__(self, other):
        if (not isinstance(other, Position)) and (not isinstance(other, Point)):
            return False
        return self.x == other.x and self.y == other.y


sqrt_2 = sqrt(2)

links = [
    Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0),
    Point(-1, -1), Point(1, -1), Point(-1, 1), Point(1, 1),
]


# 对角距离
def heuristic(p, q):
    dx = abs(p.x - q.x)
    dy = abs(p.y - q.y)
    return (dx + dy) + (sqrt_2 - 2) * min(dx, dy)


def a_star_step(open_set: PriorityQueue, close_set: set, gird, res, end, long, high):
    current = open_set.get()
    if current in close_set:
        return
    close_set.add(current)

    if current == end:
        while current is not None:
            res.append(current)
            current = current.parent
        return
    for idx, link in enumerate(links):
        point = current + link
        if point in close_set:
            continue

        if point not in open_set.queue:
            x, y = point
            if x < 0 or x > long - 1:
                continue
            if y < 0 or y > high - 1:
                continue
            if gird[y][x] < 0:
                continue

            cost = current.g + gird[y][x] + (1 if idx < 4 else sqrt_2)
            position = Position(x, y, cost, heuristic(point, end), current)
            open_set.put(position)


def a_star(gird, start: Point, end: Point, long, high):
    open_set = PriorityQueue()
    close_set = set()
    res = []
    open_set.put(Position(start.x, start.y, 0, 0))
    while not open_set.empty():
        a_star_step(open_set, close_set, gird, res, end, long, high)

    return res


def main():
    # x: 0 --- 8  9
    # y: 0 --- 5  6
    map = [
        [1, 10, 10, 10, -1, 10, 10, 10, 10],
        [10, 1, 10, 10, -1, 10, 10, 10, 10],
        [10, 10, 1, 10, -1, 10, 10, 10, 10],
        [10, 10, 10, 1, -1, 10, 10, 10, 10],
        [10, 10, 10, 10, -1, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 1, 1, 1, 1],
    ]

    print(a_star(map, Point(0, 0), Point(8, 5), 9, 6))


if __name__ == '__main__':
    main()
