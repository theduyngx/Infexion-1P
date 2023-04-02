
"""
    Authors : The Duy Nguyen (1100548) and Ramon Javier L. Felipe VI (1233281)
    File    : ids.py
    Purpose : Informed search algorithm A* to find the optimal sequence of moves for a given input state
              of a board to reach its goal state.
"""

import queue
import time
from .movement import spread
from .program import check_victory, spread
from .state import State, all_dir, MAX_VAL, PLAYER, ENEMY, SIZE
from .dist_calculator import add_direction
from .greedy_heuristic import h_greedy


def A_star(board: dict[tuple, tuple]) -> tuple: # list: #[tuple]:
    """
    A* algorithm to find the optimal sequence of moves to reach goal state
    @param board : the provided board (initial state)
    @return      : the sequence of optimal moves
    """

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
    st = time.time()
    while not open_min.empty():
        curr_state = open_min.get()
        hash_curr = curr_state.__hash__()
        del discovered[hash_curr]

        # reached goal state
        if check_victory(curr_state.board):
            et = time.time()
            return curr_state.moves, -1*(et-st)

        # for each neighboring node (direct child) of current state
        for neighbor in get_neighbors(curr_state):
            x, y, dir_x, dir_y = neighbor
            new_state = State.copy_state(curr_state)
            new_state.add_move(neighbor)

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

                # update open sets
                if hash_new not in discovered:
                    discovered[hash_new] = 1
                    open_min.put(new_state)
            
            et = time.time()
            if (et-st >= 30):
                return curr_state.moves, et-st

    et = time.time()
    return [], et-st


def get_neighbors(state: State) -> list: #[tuple]:
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


def piece_value_increment(cell: tuple) -> tuple:
    """
    For a given cell, which is a tuple in the form (position, piece), and piece is a tuple in the form
    (piece type, stack value), increment its stack value.
    @param cell : the provided cell;
    @return     : cell with incremented stack value of piece on it
    """
    tp, val = cell
    if tp == PLAYER:
        val += val < MAX_VAL
    else:
        val += 1
    return tp, val


def enemy_filter(board: dict[tuple, tuple]) -> dict[tuple, tuple]:
    """
    Filter player pieces from the board, returning only a dictionary of enemies.
    @param board : given board
    @return      : the filtered board with only enemies
    """
    return {position: piece for position, piece in board.items() if piece[0] == ENEMY}

def ally_filter(board: dict[tuple, tuple]) -> dict[tuple, tuple]:
    """
    Filter player pieces from the board, returning only a dictionary of enemies.
    @param board : given board
    @return      : the filtered board with only ally pieces
    """
    return {position: piece for position, piece in board.items() if piece[0] == PLAYER}

def h(state: State) -> int:
    """
    Heuristic function: For every piece (from most stacked to least), we check the most number of enemies
    that can be captured by it, regardless of the piece type (player or enemy). Once that is established,
    all said enemies are considered captured and will be ignored by subsequent checks.
    @param state : given current state
    @return      : the heuristic of said state (estimated number of moves to goal)
    """

    board = state.board

    # board_add increments 1 to pieces' stack: list of format (position=(x, y), piece=(type, value))
    board_add    = list(map(lambda tup: (tup[0], piece_value_increment(tup[1])), board.items()))
    sorted_board = dict(sorted(board_add, key=lambda tup: tup[1][1], reverse=True))
    enemies      = enemy_filter(board)
    num_moves    = 0
    dict_dir     = {}

    # from most stacked piece to least
    for pos in sorted_board:
        if enemies == {}:
            break
        x, y = pos
        tp, val = sorted_board[pos]

        # initialize the piece entry in direction dictionary
        for dir in all_dir:
            dict_dir[(x, y, dir)]  = []

        # for every other piece on the board - if player then player on direction
        for _pos in enemies:
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

        # remove captured enemies from list of enemies left
        for position in captured:
            del enemies[position]
        del captured
        num_moves += 1

    # cleanup
    del dict_dir
    del enemies
    del sorted_board
    del board_add
    return num_moves

# ------------------------------------- TRIM BOARD ----------------------------------------- #
def get_max_target(board: dict[tuple, tuple]) -> tuple:
    reds = ally_filter(board)
    blues = enemy_filter(board)
    new_list = []
    max_power = 0

    # First select the dominated part of the board
    if len(blues) >= len(reds):
        target = blues
        color = PLAYER
    
    else:
        target = reds
        color = ENEMY

    # Now find the pieces with highest power
    for key in target.keys():
        curr_power = board[key][1]
        if curr_power > max_power:
            max_power = curr_power
            new_list = [key]
        elif curr_power == max_power:
            new_list.append(key)
    
    return new_list, color

def greedy_red(board: dict[tuple, tuple]) -> dict[tuple, tuple]:
    all_reds = ally_filter(board=board)
    max_blues = 0
    return_dir = ()
    use_red = ()

    # Look through every red and find out which red + direction
    # captures the most blues
    for red in all_reds:
        curr_power = board[red][1]
        curr_blues = 0
        for dir in all_dir:
            dir_blues = 0
            new_pos = red
            for _ in range(curr_power):
                new_pos = add_direction(new_pos, dir)
                if new_pos in board and board[new_pos][0] == ENEMY:
                    dir_blues += 1
            if dir_blues > curr_blues:
                curr_blues = dir_blues
                local_dir = dir
        
        if curr_blues > max_blues:
            max_blues = curr_blues
            return_dir = local_dir
            use_red = red
    
    # Now after deciding that you want to spread the desired red
    # piece into the location
    _ = spread(use_red, return_dir, board)

    return board

def greedy_blue(board: dict[tuple, tuple]) -> dict[tuple, tuple]:
    # First create the dictionary for the blues
    all_blues = enemy_filter(board=board)
    all_blues = sorted(all_blues.keys(), key=lambda x: board[x][1], reverse=True)

    # Make a new dictionary for each direction
    # Dictionary will map blue and direction to closest red distance and adjacent blues
    # So (blue, dir) : (red to move, closest red dist, adjacent blues)
    blue_dict = {}


    # Iterate through all blues to find
    # the closest one 
    for blue in all_blues:
        # curr_power = board[blue][1]
        # curr_blues = 0
        # curr_red = ()
        # red_reach = 0
        new_pos = blue
        for dir in all_dir:
            blue_dict[(blue, dir)] = (0, 0)
            new_pos = blue
            red_dist = float("inf")
            adjacent_blues = 0
            move_red = ()
            curr_power = board[blue][1]
            # Iterate through all the spaces 
            for i in range(1,7):
                new_pos = add_direction(new_pos, dir)
                if new_pos in board:
                    if board[new_pos][0] == ENEMY and (curr_power-i) >= 0:
                        adjacent_blues += 1
                    elif board[new_pos][0] == PLAYER:
                        move_red = new_pos
                        red_power = board[new_pos][1]
                        red_dist = min(red_dist, abs(i-red_power)+1)
            # Now store it into the dictionary
            blue_dict[(blue, dir)] = (move_red, -1*red_dist, adjacent_blues)
    
    # Now we have to sort the dictionary based on the sum of the red_dist and adjacent_blues,
    # Ideally 

    best_blue = sorted(blue_dict.items(), key=lambda x: x[1][1] + x[1][2], reverse=True)[0]

    _ = spread(best_blue[1][0], best_blue[0][1], board)

    return board

