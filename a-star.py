from math import sqrt
from collections import namedtuple
import queue

Point = namedtuple('Point', ['x', 'y'])


class PriorityQueue(queue.PriorityQueue):
    def _init(self, maxsize):
        super(PriorityQueue, self)._init(maxsize)
        self.set = {}

    def _put(self, item):
        super(PriorityQueue, self)._put(item)
        self.set[item] = item

    def _get(self):
        item = super(PriorityQueue, self)._get()
        self.set.pop(item)
        return item


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
        return f"({self.x},{self.y})"

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


def a_star_step(open_set: PriorityQueue, close_set: set, res, target, gird, long, high):
    current = open_set.get()
    if current in close_set:
        return
    close_set.add(current)

    if current == target:
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
            position = Position(x, y, cost, heuristic(point, target), current)
            open_set.put(position)


def a_star(start: Point, end: Point, gird, long, high):
    open_set = PriorityQueue()
    close_set = set()
    res = []
    open_set.put(Position(start.x, start.y, 0, 0))
    while not open_set.empty() and not len(res):
        a_star_step(open_set, close_set, res, end, gird, long, high)

    return res, res[0].g


def double_a_star(start: Point, end: Point, gird, long, high):
    forward_open_set = PriorityQueue()
    forward_close_set = set()
    backward_open_set = PriorityQueue()
    backward_close_set = set()

    forward_res = []
    forward_open_set.put(Position(start.x, start.y, 0, 0))

    backward_res = []
    backward_open_set.put(Position(end.x, end.y, gird[end.y][end.x], 0))  # 自带地形代价

    middle = None

    def check(forward_open_set, backward_open_set):
        for item in forward_open_set.queue:
            if item in backward_open_set.set:
                return item, backward_open_set.set[item]

    while (not forward_open_set.empty()) and (not backward_open_set.empty()) and (middle is None):
        a_star_step(forward_open_set, forward_close_set, forward_res, end, gird, long, high)
        middle = check(forward_open_set,backward_open_set)
        if middle:
            break
        a_star_step(backward_open_set, backward_close_set, backward_res, start, gird, long, high)
        middle = check(forward_open_set, backward_open_set)

    forward, backword = middle
    res = []

    while forward is not None:
        res.append(forward)
        forward = forward.parent

    while backword is not None:
        backword = backword.parent
        if backword is not None:
            res.insert(0, backword)

    return res, middle[0].g + middle[1].g - gird[middle[0].y][middle[0].x]


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

    print(a_star(Point(0, 0), Point(8, 5), map, 9, 6))
    print(double_a_star(Point(0, 0), Point(8, 5), map, 9, 6))


if __name__ == '__main__':
    main()
