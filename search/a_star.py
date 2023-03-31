# IMPORTS
import queue
from program import check_victory, spread
from state import *
from dist_calculator import add_direction


def A_star(board: dict[tuple, tuple]) -> [tuple]:
    """
    A* algorithm to find the optimal sequence of moves to reach goal state

    @param board : the provided board (initial state)
    @return      : the sequence of optimal moves
    """
    min_found = queue.PriorityQueue()  # discovered nodes
    g_cost = {}  # real cumulative cost from root
    f_cost = {}  # best guess f = g + h
    discovered = {}

    curr_state = State(board, [], 0)
    hash_curr = curr_state.__hash__()
    min_found.put(curr_state)  # init state has now been discovered
    discovered[hash_curr] = 1
    g_cost[hash_curr] = 0
    f_cost[hash_curr] = 0
    # min_moves = []
    # num_moves = INF

    while not min_found.empty():
        curr_state = min_found.get()
        hash_curr = curr_state.__hash__()
        del discovered[hash_curr]
        if check_victory(curr_state.board):
            return curr_state.moves
            # return the optimal moves to reach the goal state
            # if len(curr_state.moves) < num_moves:
            #     min_moves = curr_state.moves
            #     num_moves = len(curr_state.moves)

        for neighbor in get_neighbors(curr_state):
            x, y, dir_x, dir_y = neighbor
            new_state = State.copy_state(curr_state)
            new_state.add_move(neighbor)
            _ = spread(position=(x, y), direction=(dir_x, dir_y), board=new_state.board)
            hash_new = new_state.__hash__()
            # true cost from init to new_state via curr_state
            g_cost_accum = g_cost[hash_curr] + 1

            if hash_new not in g_cost or g_cost_accum < g_cost[hash_new]:
                g_cost[hash_new] = g_cost_accum
                f_cost[hash_new] = g_cost_accum + h(new_state)
                new_state.f_cost = f_cost[hash_new]
                if hash_new not in discovered:
                    discovered[hash_new] = 1
                    min_found.put(new_state)
    return []


def h(state: State) -> int:
    """
    The heuristic function.

    @param state : given current state
    @return      : the heuristic of said state (estimated number of moves to goal)
    """
    return h2(state)


def h1(state: State) -> int:
    total_heuristic = 0

    # Get all the pieces
    curr_board = state.board

    # First store the pieces in the board from biggest to smallest
    board_add = list(map(lambda tup: (tup[0], h_add(tup[1])), curr_board.items()))
    enemies = [pos for pos in curr_board.keys() if curr_board[pos][0] == ENEMY]
    sorted_board = sorted(board_add, key=lambda x: x[1][1], reverse=True)
    captured_pieces = {}

    # Now iterate through the list
    for piece, _ in sorted_board:
        if len(captured_pieces.keys()) >= len(enemies):
            break
        add, captured_pieces = h1_adjacent_blues(curr_board, piece, captured_pieces)
        total_heuristic += add

    # Once that is all done, check if there are any blues
    # not_captured = len([key for key in captured_pieces.keys() if captured_pieces[key] == False])
    not_captured = len(captured_pieces.keys()) == len(curr_board.keys())
    total_heuristic += not_captured

    return total_heuristic


# Helper function for incrementing power in the board
def h_add(cell: tuple) -> tuple:
    tp, val = cell
    if tp == PLAYER:
        if val < MAX_VAL:
            val += 1
    else:
        val += 1
    return tp, val


# Helper funct for h1
# Edited this adjacent blues for the new heuristic h1
def h1_adjacent_blues(board: dict[tuple, tuple], piece: tuple, captured: dict) -> tuple:
    _, curr_power = board[piece]
    new_captures = {}
    max_blues = 0

    # Check all directions for the max
    for dir in all_dir:
        curr_blues = 0
        new_enemy = piece
        curr_captures = {}
        for _ in range(curr_power):
            new_enemy = add_direction(new_enemy, dir)
            if new_enemy in board:
                if board[new_enemy][0] == ENEMY:
                    curr_blues += new_enemy not in captured
                    curr_captures[new_enemy] = True

        # Need to adjust both our current max and the blues we will add to captured list
        if curr_blues > max_blues:
            max_blues = curr_blues
            new_captures = curr_captures
        del curr_captures

    # Max Blues being greater than 0 means a capture did occur
    if max_blues > 0:
        for item in new_captures.keys():
            captured[item] = True
        del new_captures
        return 1, captured

    del new_captures
    return 0, captured


# --------------------------- h2 -------------------------------- #


def enemy_filter(board: dict[tuple, tuple]) -> dict[tuple, tuple]:
    return {position: piece for position, piece in board.items() if piece[0] == ENEMY}


def h2(state: State) -> int:
    """
    Heuristic function 2 - checking enemies in line (single direction) with no regards to the stack
    value of the pieces.

    @param state : given current state
    @return      : the heuristic of said state (estimated number of moves to goal)
    """

    board = state.board

    # board_add adds 1 to pieces: list of (position=(x, y), piece=(type, value))
    board_add = list(map(lambda tup: (tup[0], h_add(tup[1])), board.items()))
    sorted_board = dict(sorted(board_add, key=lambda tup: tup[1][1], reverse=True))
    enemies = enemy_filter(board)

    num_moves = 0
    dict_dir = {}

    for pos in sorted_board:
        if enemies == {}:
            break
        x, y = pos
        tp, val = sorted_board[pos]
        if tp == PLAYER:
            val += val < MAX_VAL
        else:
            val += 1
            if val == SIZE:
                continue

        # initialize the piece entry in direction dictionary
        for dir in all_dir:
            dict_dir[(x, y, dir)]  = []

        # for every other piece on the board - if player then player on direction
        for _pos in enemies:
            _x, _y = _pos
            _tp, _ = board[_pos]

            # x-direction
            x_diff = x - _x
            y_diff = y - _y
            xd_abs = abs(x_diff)
            yd_abs = abs(y_diff)
            if _x == x and _y != y:
                sign = int(y_diff / yd_abs)
                if yd_abs <= val:
                    dict_dir[(x, y, (0, sign))].append(_pos)
                if yd_abs <= SIZE - val:
                    dict_dir[(x, y, (0, -sign))].append(_pos)

            # y-direction
            elif _x != x and _y == y:
                sign = int(x_diff / xd_abs)
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
                if diff == 0 or diff == SIZE:
                    dict_dir[(x, y, (x_sign, y_sign))].append(_pos)
                    if larger <= val:
                        dict_dir[(x, y, (-x_sign, -y_sign))].append(_pos)

        # list out to reduce overhead
        max_captured = 0
        captured = []
        for dir in all_dir:
            curr_len = len(dict_dir[(x, y, dir)])
            if curr_len > max_captured:
                max_captured = curr_len
                captured = dict_dir[(x, y, dir)]

        if not captured:
            if pos in enemies:
                num_moves += 1
            continue

        for position in captured:
            del enemies[position]
        num_moves += 1

    del dict_dir
    del sorted_board
    del board_add
    return num_moves


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
