"""
    Authors : The Duy Nguyen (1100548) and Ramon Javier L. Felipe VI (1233281)
    Module  : a_star.py
    Purpose : Informed search algorithm A* to find the optimal sequence of moves for a given input state
              of a board to reach its goal state.
"""

import queue
import heapq
from movement import *
from state import *


def informed_search(board: dict[tuple, tuple]) -> [tuple]:
    """
    Informed search algorithm - hybrid algorithm using primarily A*, among other informed algorithms
    in special cases.

    @param board : the given board
    @return      : the optimal sequence of moves to reach goal state
    """
    all_1 = (len(board) == TOTAL)
    if not all_1 and len(board) >= DENSE:
        for pos in board:
            tp, val = board[pos]
            if tp == ENEMY and val != MIN_VAL:
                all_1 = False
                break
            all_1 = True
    if all_1:
        return greedy_search(board)
    return A_star(board, debug=True)


# ------------------------------------- GREEDY SEARCH ----------------------------------------- #


def player_filter(board: dict[tuple, tuple]) -> dict[tuple, tuple]:
    """
    Filter player pieces from the board, returning only a dictionary of enemies.

    @param board : given board
    @return      : the filtered board with only enemies
    """
    return {position: piece for position, piece in board.items() if piece[0] == PLAYER}


def greedy_search(board: dict[tuple, tuple]) -> list[tuple]:
    """
    Greedy search algorithm in the special case of all enemy pieces have value of 1. The first priority is to
    capture as many enemies as possible, and the second is to leave as little number of scattered enemies on
    the board as possible. Not optimal.

    @param board : the given board
    @return      : optimal sequence of moves to reach goal state
    """
    board_copy = board.copy()
    moves = []
    while not check_victory(board_copy):

        # max-heapify the board
        player_filtered = player_filter(board_copy)
        player_heap     = list(map(lambda tup: (-tup[1][1], tup[0]), player_filtered.items()))
        heapq.heapify(player_heap)
        max_captured  = 0
        min_scattered = INF
        move_pos      = ()
        move_to       = ()

        # now instead of looping in pos, we pop the max constantly until
        # we get the number of blues captured that match the current max
        while player_heap:
            curr = heapq.heappop(player_heap)
            neg_val, pos = curr
            val = abs(neg_val)
            found = not player_heap

            # for each direction, we check which move would fill up a number of enemies that is equal to
            # the stack value of the current player piece
            for dir in all_dir:

                # if the maximum number of captured already exceeds the current stack value
                if max_captured > val:
                    found = True
                    break

                # get the number of captured and scattered enemies as a result of spread
                num_captured, num_scattered = get_captured_and_scattered(board_copy, pos, dir)

                # if it exceeds current max number of captured but not fully fulfilling its potential
                if num_captured > max_captured:
                    max_captured = num_captured
                    move_to = dir
                    move_pos = pos
                    min_scattered = num_scattered

                # if number of captured enemies is equal to current max, we consider the second priority
                elif num_captured == max_captured > 0:
                    if num_scattered < min_scattered:
                        move_to = dir
                        move_pos = pos
                        min_scattered = num_scattered

            # we found the direction to move to, append to move list
            if found:
                spread(move_pos, move_to, board_copy)
                x, y = move_pos
                dir_x, dir_y = move_to
                moves.append((x, y, dir_x, dir_y))
                break
    return moves


def move_increment_by_direction(pos: tuple, dir: tuple) -> tuple:
    """
    Move a piece on given position by 1 move as per the given direction.

    @param pos : given position of to-move piece
    @param dir : the move direction
    @return    : new position
    """
    tmp_pos = [INF, INF]
    for i in range(2):
        new_val = pos[i] + dir[i]
        if new_val > MAX_VAL:
            new_val = new_val - SIZE
        elif new_val < 0:
            new_val = SIZE + new_val
        tmp_pos[i] = new_val
    return tuple(tmp_pos)


def get_captured_and_scattered(board: dict[tuple, tuple], player_pos: tuple, player_dir: tuple) -> tuple:
    """
    Get the number of captured enemies, and scattered (isolated from other enemies) as a result of a specific
    spread move.

    @param board      : given board
    @param player_pos : player position where spread move
    @param player_dir : the direction of the spread move
    @return           : number of enemies captured from spread, and number of scattered enemies
    """

    if player_pos not in board:
        return ()
    num_captured  = 0
    num_scattered = 0
    captured_pos  = player_pos
    _, player_val = board[player_pos]

    for i in range(player_val):
        x_capt_dir, y_capt_dir = player_dir
        if i > 0:
            x_capt_dir = -x_capt_dir
            y_capt_dir = -y_capt_dir
        captured_pos = move_increment_by_direction(captured_pos, player_dir)
        if captured_pos not in board:
            continue
        tp, _ = board[captured_pos]
        if tp == PLAYER:
            continue

        # we found an enemy captured piece, now we must find if this leaves any isolated enemies
        num_captured += 1

        # for each direction of captured position, we get its adjacent piece
        for dir in all_dir:
            if dir == (x_capt_dir, y_capt_dir):
                continue
            adjacent_captured = move_increment_by_direction(captured_pos, dir)
            if adjacent_captured in board:
                tp, val = board[adjacent_captured]

                # we don't care about adjacents that are player pieces
                if tp == PLAYER:
                    continue

                # for each adjacents of said (captured enemy's) adjacent, we have to check whether there are
                # no enemy pieces adjacent to it or not
                no_adjacents = True
                for new_dir in all_dir:
                    new_pos = move_increment_by_direction(adjacent_captured, new_dir)

                    # if adjacent piece goes back to captured position, we skip
                    if new_pos == captured_pos:
                        continue

                    # if the interested position is in the board
                    if new_pos in board:
                        new_tp, _ = board[new_pos]
                        # then we must make sure if enemy then there are adjacents after all
                        if new_tp == ENEMY:
                            no_adjacents = False
                            break
                num_scattered += no_adjacents
    return num_captured, num_scattered


# ------------------------------------- A-STAR SEARCH ----------------------------------------- #


def A_star(board: dict[tuple, tuple], debug=False) -> [tuple]:
    """
    A* algorithm to find the optimal sequence of moves to reach goal state

    @param board : the provided board (initial state)
    @param debug : debug mode printing out number of node generations
    @return      : the sequence of optimal moves
    """

    num_operations = 0

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
        hash_curr = curr_state.__hash__()
        del discovered[hash_curr]

        # reached goal state
        if check_victory(curr_state.board):
            if debug:
                print("Number of generations is", num_operations)
            return curr_state.moves

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

                # update open sets
                if hash_new not in discovered:
                    discovered[hash_new] = 1
                    open_min.put(new_state)
    return []


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

    # dictionaries to keep track of direction captures
    dict_dir = {}
    max_captured = []

    # EDIT:
    # now for each captured direction, we don't delete the entries immediately like we are doing now
    # unless the entry has length 0 (meaning no captured possible).

    # If the number of captured == the stack value of piece, then it has fulfilled its potential and we can
    # delete it as per usual and update captured dictionary

    # Otherwise, we must keep those entries, push to a heap and move on; heap entry:
    # (length of list of captured pieces (L), position, captured list)

    # We move on to the next highest stack value (sorted board)
    # if the stack value of that is less than L of heap[0] (don't pop it yet): then that means our current
    # highest stack is already lower than most potential currently anyway so we pop, num_moves += 1 and update
    # the captured dictionary

    # else, we do the same thing.
    # Until either the captured dictionary is empty, or the heap is empty

    # ANOTHER important aspect is that when sorting the sorted board list, red with equal value to blue must
    # precede it (more prioritized in other words) --> DONE!!

    # from most stacked piece to least
    for pos in sorted_board:
        if not uncaptured:
            break
        x, y = pos
        tp, val = sorted_board[pos]
        moved = False

        # check if val less than current highest potential of max_captured
        # not quite correct yet, after this we must check to make sure the length of the captured list is corrected
        # since we don't know if there are enemy pieces already captured by something else from before
        if val < max_captured[0][0]:
            num_captured, entry = heapq.heappop(max_captured)
            x_moved, y_moved, dir_moved = entry

            # remove stuffs in dict_dir
            for dir in all_dir:
                entry = dict_dir[(x_moved, y_moved, dir)]
                if moved or not entry:
                    del entry

            # remove captured enemies from all un-captured enemies
            captured = dict_dir[(x_moved, y_moved, dir_moved)]
            for position in captured:
                # if moved fulfils potential then we delete enemies from uncaptured and dict_dir entries
                del uncaptured[position]

            # remove unnecessary
            num_moves += 1
            continue

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
        num_captured = 0
        captured = []
        for dir in all_dir:
            curr_len = len(dict_dir[(x, y, dir)])
            if curr_len > num_captured:
                num_captured = curr_len
                captured = dict_dir[(x, y, dir)]
            if num_captured == val:
                moved = True
                break

        # if no capture
        if not captured:
            continue

        # remove stuffs in dict_dir
        for dir in all_dir:
            entry = dict_dir[(x, y, dir)]
            if moved or not entry:
                del entry
            else:
                heap_entry = len(entry), (x, y, dir)
                heapq.heappush(max_captured, heap_entry)

        # remove captured enemies from all un-captured enemies
        if moved:
            for position in captured:
                # if moved fulfils potential then we delete enemies from uncaptured and dict_dir entries
                del uncaptured[position]
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
    sorted_board = dict(sorted(board_add, key=lambda tup: tup[1][1], reverse=True))
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
