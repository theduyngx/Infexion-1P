# Python Equivalent
import math

INF = 9999


# A structure to represent a Point in 2D plane
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # def __init__(self, tup: tuple):
    #     (x, y) = tup
    #     self.x = x
    #     self.y = y

    def to_tuple(self):
        return self.x, self.y


# A utility function to find the distance between two points
def dist(p1: Point, p2: Point) -> float:
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


# A Brute Force method to return the smallest distance between two points in P[] of size n
def brute_force(points: [Point], n: int) -> (Point, Point, float):
    global ret
    min_dist = INF
    for i in range(n):
        for j in range(i + 1, n):
            curr_dist = dist(points[i], points[j])
            if curr_dist < min_dist:
                min_dist = curr_dist
                ret = (points[i], points[j], min_dist)
    return ret


# A utility function to find distance between the closest points of strip of a given size.
# All points in strip[] are sorted according to y coordinate. They all have upper bound on
# minimum distance as d. Note that this method is O(n), as inner loop runs at most n times.
def strip_closest(strip: [Point], sd: float) -> (Point, Point, float):
    global ret
    min_dist = sd
    size = len(strip)

    for i in range(size):
        for j in range(i + 1, size):
            if (strip[j].y - strip[i].y) >= min_dist:
                break
            curr_dist = dist(strip[i], strip[j])
            if curr_dist < min_dist:
                min_dist = curr_dist
                ret = (strip[i], strip[j], min_dist)
    return ret


# A recursive function to find the smallest distance. The array xs contains all points sorted
# according to x coordinates and ys contains all points sorted according to y coordinates
def closest_util(xs: [Point], ys: [Point], n: int) -> (Point, Point, float):
    global pd1, pd2, d

    if n <= 3:
        return brute_force(xs, n)
    mid = n // 2
    mid_point = xs[mid]

    # Divide points in y sorted array around the vertical line.
    # Assumption: All x coordinates are distinct.
    ysl = [None] * mid          # y sorted points on left of vertical line
    ysr = [None] * (n - mid)    # y sorted points on right of vertical line
    li = ri = 0                 # indexes of left and right sub-arrays
    for i in range(n):
        if li < mid and (ys[i].x < mid_point.x or (ys[i].x == mid_point.x and ys[i].y < mid_point.y)):
            ysl[li] = ys[i]
            li += 1
        elif ri < n - mid:
            ysr[ri] = ys[i]
            ri += 1

    # Consider the vertical line passing through the middle point calculate the smallest distance dl
    # on left of middle point and dr on right side
    pl1, pl2, dl = closest_util(xs, ysl, mid)
    pr1, pr2, dr = closest_util(xs[mid:], ysr, n - mid)
    if dl < dr:
        d   = dl
        pd1 = pl1
        pd2 = pl2
    else:
        d   = dr
        pd1 = pr1
        pd2 = pr2

    # Build an array strip[] that contains points close (closer than d) to the line passing through
    # the middle point
    strip = []
    for i in range(n):
        if abs(ys[i].x - mid_point.x) < d:
            strip.append(ys[i])

    # Find the closest points in strip.  Return the minimum of d and closest distance is strip[]
    ps1, ps2, s = strip_closest(strip, d)
    if d < s:
        return pd1, pd2, d
    return ps1, ps2, s


def closest(points: [Point], n: int) -> (Point, Point, float):
    """
    Finds the closest distance of any given 2 pieces of opposite colors.

    @param points:
    @param n:
    @return:
    """
    xs = sorted(points, key=lambda p: p.x)
    ys = sorted(points, key=lambda p: p.y)

    # Use recursive function closest_util() to find the smallest distance
    return closest_util(xs, ys, n)


# Driver program to test above functions
if __name__ == '__main__':
    P = [Point(2, 3), Point(12, 3), Point(40, 50), Point(5, 1), Point(12, 10), Point(3, 4), Point(16, 2), Point(55, 2),
         Point(54.5, 1.9), Point(0, 2), Point(0.01, 5), Point(0.01, 1.99), Point(6, 6), Point(60, 60)]
    length = len(P)
    point1, point2, distance = closest(P, length)
    print("The smallest distance is", distance, "for", Point.to_tuple(point1), "and", Point.to_tuple(point2))
