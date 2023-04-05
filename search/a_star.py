"""
    Authors : The Duy Nguyen (1100548) and Ramon Javier L. Felipe VI (1233281)
    Module  : a_star.py
    Purpose : A* search strategy to find the optimal path to reach goal state. Makes use of dynamic
              heuristic depending on the density of the board.
"""

import queue
from state import *
from movement import spread
from sequence import Sequence


def A_star(board: dict[tuple, tuple]) -> Sequence:
    """
    A* algorithm to find the optimal sequence of moves to reach goal state

    @param board : the provided board (initial state)
    @return      : object sequence, representing the optimal sequence of moves
    """

    num_operations = 0
    mem_use = len(board)

    open_min   = queue.PriorityQueue()  # open set ordered by minimal cost first
    g_cost     = {}                     # real cumulative cost from root
    f_cost     = {}                     # best guess f = g + h
    discovered = {}                     # open set - set of all generated but un-expanded nodes

    curr_state = State(board, [], 0)    # current state initialized as init state
    hash_curr  = curr_state.__hash__()  # hashed state for dictionary accessing
    open_min.put(curr_state)            # init state has now been discovered
    discovered[hash_curr] = 1
    g_cost[hash_curr]     = 0           # real cost from init state
    f_cost[hash_curr]     = 0           # f cost from init to goal state

    # by using min-heap, we can immediately retrieve unexpanded nodes with lowest f-score
    while not open_min.empty():
        curr_state = open_min.get()
        hash_curr  = curr_state.__hash__()
        del discovered[hash_curr]
        mem_use -= (len(curr_state.board) + len(curr_state.moves))

        # reached goal state
        if check_victory(curr_state.board):
            mem_use += len(discovered) + len(g_cost) + len(f_cost)
            sequence = Sequence(curr_state.moves, num_operations, mem_use, A_star.__name__)
            return sequence

        # for each neighboring node (direct child) of current state
        for neighbor in get_neighbors(curr_state):
            x, y, dir_x, dir_y = neighbor
            new_state = State.copy_state(curr_state)
            new_state.add_move(neighbor)
            num_operations += 1

            # each neighbor is a state resulted by single player move from current state
            spread(position=(x, y),
                   direction=(dir_x, dir_y),
                   board=new_state.board)
            hash_new = new_state.__hash__()

            # true cost from init to new_state via curr_state
            g_cost_accum = g_cost[hash_curr] + 1
            if hash_new not in g_cost or g_cost_accum < g_cost[hash_new]:
                g_cost[hash_new] = g_cost_accum
                f_cost[hash_new] = g_cost_accum + h(new_state)
                new_state.f_cost = f_cost[hash_new]

                # update open sets --> update memory use
                if hash_new not in discovered:
                    discovered[hash_new] = 1
                    open_min.put(new_state)
                    mem_use += len(new_state.board) + len(new_state.moves)

    sequence = Sequence([], num_operations, mem_use, A_star.__name__)
    return sequence


def get_neighbors(state: State) -> [tuple]:
    """
    Get all neighboring state of a given, current state of the board. Neighbors are all derived states
    resulted from player's single move.

    @param state : given current state
    @return      : list of all possible single move by player that returns a neighboring state
    """
    neighbors = []
    board = state.board
    for x, y in board.keys():
        p_type, stack = board[(x, y)]
        if p_type == ENEMY:
            continue
        for dir_x, dir_y in all_dir:
            neighbors.append((x, y, dir_x, dir_y))
    return neighbors


# ------------------------------------- HEURISTIC ----------------------------------------- #


def piece_value_increment(cell: tuple, num_player: int) -> tuple:
    """
    For a given cell, which is a tuple in the form (position, piece), and piece is a tuple in the form
    (piece type, stack value), increment its stack value.

    @param cell       : the provided cell
    @param num_player : number of player pieces
    @return           : cell with incremented stack value of piece on it
    """
    tp, val = cell
    if tp == PLAYER:
        val += (val < MAX_VAL) * (num_player > 1)
    else:
        val += 1
        if val >= SIZE:
            val -= SIZE
    return tp, val


def enemy_filter(board: dict[tuple, tuple]) -> dict[tuple, tuple]:
    """
    Filter player pieces from the board, returning only a dictionary of enemies.

    @param board : given board
    @return      : the filtered board with only enemies
    """
    return {position: piece for position, piece in board.items() if piece[0] == ENEMY}


def h(state: State) -> int:
    """
    Heuristic function: a hybrid, dynamic heuristic that applies different function depending on the
    density of the board.

    @param state : the given state of the board
    @return      : the heuristic of said state (estimated number of moves to goal)
    """
    if len(state.board) >= DENSE:
        return h2(state)
    return h1(state)


def h1(state: State) -> int:
    """
    Heuristic function for sparse state:
    For every piece (from most stacked to least), we check the most number of enemies
    that can be captured by it, regardless of the piece type (player or enemy). Once that is established,
    all said enemies are considered captured and will be ignored by subsequent checks.

    @param state : given current state
    @return      : the heuristic of said state (estimated number of moves to goal)
    """

    board = state.board

    # board_add increments 1 to pieces' stack: list of format (position=(x, y), piece=(type, value))
    uncaptured   = enemy_filter(board)
    num_player   = len(board) - len(uncaptured)
    board_add    = list(map(lambda tup: (tup[0], piece_value_increment(tup[1], num_player)), board.items()))
    sorted_board = dict(sorted(board_add, key=lambda tup: (tup[1][1], tup[1][0]), reverse=True))
    num_moves    = 0
    dict_dir     = {}

    # from most stacked piece to least
    for pos in sorted_board:
        if not uncaptured:
            break
        x, y = pos
        tp, val = sorted_board[pos]

        # initialize the piece entry in direction dictionary
        for dir in all_dir:
            dict_dir[(x, y, dir)] = []

        # for every un-captured enemy
        for _pos in uncaptured:
            _x, _y = _pos
            _tp, _ = board[_pos]
            x_diff = x - _x
            y_diff = y - _y
            xd_abs = abs(x_diff)
            yd_abs = abs(y_diff)

            # x-direction
            if _x == x and _y != y:
                sign = int(y_diff / yd_abs)

                # add to both directions of x-direction if stack is sufficiently large
                if yd_abs <= val:
                    dict_dir[(x, y, (0, sign))].append(_pos)
                if yd_abs <= SIZE - val:
                    dict_dir[(x, y, (0, -sign))].append(_pos)

            # y-direction
            elif _x != x and _y == y:
                sign = int(x_diff / xd_abs)

                # add to both directions of y-direction if stack is sufficiently large
                if xd_abs <= val:
                    dict_dir[(x, y, (sign, 0))].append(_pos)
                if xd_abs <= SIZE - val:
                    dict_dir[(x, y, (-sign, 0))].append(_pos)

            # vertical direction
            elif _x != x:
                diff = abs(x_diff + y_diff)
                if xd_abs < yd_abs:
                    x_sign = 1
                    larger = yd_abs
                else:
                    x_sign = -1
                    larger = xd_abs
                y_sign = -x_sign

                # add to both directions of vertical direction if stack is sufficiently large
                if diff == 0 or diff == SIZE:
                    dict_dir[(x, y, (x_sign, y_sign))].append(_pos)
                    if larger <= val:
                        dict_dir[(x, y, (-x_sign, -y_sign))].append(_pos)

        # check the direction with most captures
        max_captured = 0
        captured = []
        for dir in all_dir:
            curr_len = len(dict_dir[(x, y, dir)])
            if curr_len > max_captured:
                max_captured = curr_len
                captured = dict_dir[(x, y, dir)]

        # if no capture
        if not captured:
            continue

        # remove captured enemies from all un-captured enemies
        for position in captured:
            del uncaptured[position]
        del captured
        num_moves += 1

    num_moves += (uncaptured != {})

    # cleanup
    del dict_dir
    del uncaptured
    del sorted_board
    del board_add
    return num_moves


def h2(state: State) -> int:
    """
    Heuristic function for dense state:
    Only check for stacked pieces. The rest uncaptured enemies will be calculated differently.

    @param state : given current state
    @return      : the heuristic of said state (estimated number of moves to goal)
    """

    board = state.board

    # board_add increments 1 to pieces' stack: list of format (position=(x, y), piece=(type, value))
    uncaptured   = enemy_filter(board)
    num_player   = len(board) - len(uncaptured)
    board_add    = list(map(lambda tup: (tup[0], piece_value_increment(tup[1], num_player)), board.items()))
    sorted_board = dict(sorted(board_add, key=lambda tup: (tup[1][1], tup[1][0]), reverse=True))
    num_moves    = 0
    dict_dir     = {}

    # from most stacked piece to least
    for pos in sorted_board:
        if not uncaptured:
            break
        x, y = pos
        tp, val = sorted_board[pos]

        # break if reached 1
        if val <= MIN_VAL + 1:
            break

        # initialize the piece entry in direction dictionary
        for dir in all_dir:
            dict_dir[(x, y, dir)] = []

        # for every un-captured enemy
        for _pos in uncaptured:
            _x, _y = _pos
            _tp, _ = board[_pos]
            x_diff = x - _x
            y_diff = y - _y
            xd_abs = abs(x_diff)
            yd_abs = abs(y_diff)

            # x-direction
            if _x == x and _y != y:
                sign = int(y_diff / yd_abs)

                # add to both directions of x-direction if stack is sufficiently large
                if yd_abs <= val:
                    dict_dir[(x, y, (0, sign))].append(_pos)
                if yd_abs <= SIZE - val:
                    dict_dir[(x, y, (0, -sign))].append(_pos)

            # y-direction
            elif _x != x and _y == y:
                sign = int(x_diff / xd_abs)

                # add to both directions of y-direction if stack is sufficiently large
                if xd_abs <= val:
                    dict_dir[(x, y, (sign, 0))].append(_pos)
                if xd_abs <= SIZE - val:
                    dict_dir[(x, y, (-sign, 0))].append(_pos)

            # vertical direction
            elif _x != x:
                diff = abs(x_diff + y_diff)
                if xd_abs < yd_abs:
                    x_sign = 1
                    larger = yd_abs
                else:
                    x_sign = -1
                    larger = xd_abs
                y_sign = -x_sign

                # add to both directions of vertical direction if stack is sufficiently large
                if diff == 0 or diff == SIZE:
                    dict_dir[(x, y, (x_sign, y_sign))].append(_pos)
                    if larger <= val:
                        dict_dir[(x, y, (-x_sign, -y_sign))].append(_pos)

        # check the direction with most captures
        max_captured = 0
        captured = []
        for dir in all_dir:
            curr_len = len(dict_dir[(x, y, dir)])
            if curr_len > max_captured:
                max_captured = curr_len
                captured = dict_dir[(x, y, dir)]

        # if no capture
        if not captured:
            continue

        # remove captured enemies from all un-captured enemies
        for position in captured:
            del uncaptured[position]
        del captured
        num_moves += 1

    num_moves += len(uncaptured) - (len(uncaptured) % 2)

    # cleanup
    del dict_dir
    del uncaptured
    del sorted_board
    del board_add
    return num_moves
