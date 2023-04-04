"""
    Authors : The Duy Nguyen (1100548) and Ramon Javier L. Felipe VI (1233281)
    Module  : greedy_search.py
    Purpose : Greedy search strategy for very dense boards with a condition that all enemies must have
              power value of 1.
"""

import heapq
from state import *
from movement import spread


def player_filter(board: dict[tuple, tuple]) -> dict[tuple, tuple]:
    """
    Filter player pieces from the board, returning only a dictionary of enemies.

    @param board : given board
    @return      : the filtered board with only enemies
    """
    return {position: piece for position, piece in board.items() if piece[0] == PLAYER}


def Greedy_search(board: dict[tuple, tuple]) -> (int, list[tuple]):
    """
    Greedy search algorithm in the special case of all enemy pieces have value of 1. The first priority is to
    capture as many enemies as possible, and the second is to leave as little number of scattered enemies on
    the board as possible. Not optimal.

    @param board : the given board
    @return      : the number of generations required,
                   and the optimal sequence of moves to reach goal state
    """

    num_operations = 0

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
            num_operations += 1

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
    return num_operations, moves


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
