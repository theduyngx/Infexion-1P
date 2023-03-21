# Python Equivalent
from math import sqrt
from board import *

INF = 9999


def dist(c1: Cell, c2: Cell) -> float:
    """
    Euclidean distance between 2 cells on the board.

    @param c1: cell 1
    @param c2: cell 2
    @return  : euclidean distance between the cells
    """
    return sqrt((c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2)


def closest_brute_force(cells: [Cell]) -> (Cell, Cell, float):
    """
    Brute force method to find the closest distance between 2 cells on the board.

    @param cells : list of cells to brute force and find the closest distance
    @return      : cell of the first piece,
                   cell of the second piece,
                   the distance from said cells (which would be the closest)
    """
    global ret
    min_dist = INF
    n = len(cells)
    for i in range(n):
        for j in range(i + 1, n):
            curr_dist = dist(cells[i], cells[j])
            # if closer distance found and only if type of pieces are different
            if curr_dist < min_dist and cells[i].type != cells[j].type:
                min_dist = curr_dist
                ret = (cells[i], cells[j], min_dist)
    return ret


def closest_strip(strip: [Cell], sd: float) -> (Cell, Cell, float):
    """
    Find distance between the closest cells of a strip of a given width. The cells in
    strip are sorted by y-coordinate.

    @param strip: the given strip (a stripped down area of only viable cells).
    @param sd   : the given width of the strip
    @return     : cell of the first piece,
                  cell of the second piece,
                  the distance from said cells (which would be the closest)
    """
    global ret
    min_dist = sd
    size = len(strip)

    for i in range(size):
        for j in range(i + 1, size):
            if (strip[j].y - strip[i].y) >= min_dist:
                break
            curr_dist = dist(strip[i], strip[j])
            # if closer distance found and only if type of pieces are different
            if curr_dist < min_dist and strip[i].type != strip[j].type:
                min_dist = curr_dist
                ret = (strip[i], strip[j], min_dist)
    return ret


def closest_util(xs: [Cell], ys: [Cell]) -> (Cell, Cell, float):
    """
    Check recursively for the closest distance - recursion is based on the band surrounding the
    vertical midpoint line where the interested cells are is reduced whenever a closer distance
    is found.

    @param xs : list of cells sorted by x-coordinate
    @param ys : list of cells sorted by y-coordinate
    @return   : cell of the first piece,
                cell of the second piece,
                the distance from said cells (which would be the closest)
    """

    global cd1, cd2, d
    n = len(ys)
    if n <= 3:
        return closest_brute_force(xs)
    mid = n // 2
    mid_point = xs[mid]

    ysl_size = mid
    ysr_size = n - mid
    ysl = [None] * ysl_size     # y sorted cells on left of vertical line
    ysr = [None] * ysr_size     # y sorted cells on right of vertical line
    li = ri = 0                 # indices of left and right sub-arrays, respectively
    for i in range(n):
        if li < ysl_size and (ys[i].x < mid_point.x or (ys[i].x == mid_point.x and ys[i].y < mid_point.y)):
            ysl[li] = ys[i]
            li += 1
        elif ri < ysr_size:
            ysr[ri] = ys[i]
            ri += 1

    # Consider the vertical line passing through the middle cell
    # --> calculate the closest distance dl on LHS and dr on RHS
    cl1, cl2, dl = closest_util(xs, ysl)
    cr1, cr2, dr = closest_util(xs[mid:], ysr)
    if dl < dr:
        d   = dl
        cd1 = cl1
        cd2 = cl2
    else:
        d   = dr
        cd1 = cr1
        cd2 = cr2

    # strip is list containing cells closer than d to the vertical midpoint line
    strip = []
    for i in range(n):
        if abs(ys[i].x - mid_point.x) < d:
            strip.append(ys[i])

    # Find the closest cells in strip
    cs1, cs2, s = closest_strip(strip, d)
    if d < s:
        return cd1, cd2, d
    return cs1, cs2, s


def closest(cells: [Cell]) -> (Cell, Cell, float):
    """
    Finds the closest distance of any given 2 pieces of opposite colors.

    @param cells : list of all occupied cells, essentially the current state of the board
    @return      : cell of the first piece,
                   cell of the second piece,
                   the distance from said cells (which would be the closest)
    """
    xs = sorted(cells, key=lambda p: p.x)
    ys = sorted(cells, key=lambda p: p.y)

    # Use recursive function closest_util() to find the smallest distance
    return closest_util(xs, ys)


# testing
if __name__ == '__main__':
    board = {
        (5, 6): ("r", 2),
        (1, 0): ("b", 2),
        (1, 1): ("b", 1),
        (3, 2): ("b", 1),
        (1, 3): ("b", 3),
        (4, 1): ("r", 3),
        (2, 4): ("b", 6),
        (2, 5): ("b", 3)
    }
    P = []
    for pos in board:
        P.append(Cell(pos, board[pos]))
    cell1, cell2, distance = closest(P)
    print("The smallest distance is", distance, "for", Cell.to_tuple(cell1), "and", Cell.to_tuple(cell2))
