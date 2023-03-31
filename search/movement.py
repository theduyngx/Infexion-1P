# Author  : The Duy Nguyen (1100548) and Ramon Javier L. Felipe VI (1233281)
# File    : movement.py
# Purpose : Including functions related to moving a piece on the board.

from state import *
from utils import render_board


def spread(position: tuple, direction: tuple, board: dict[tuple, tuple]) -> bool:
    """
    SPREAD movement for a specified piece.

    @param position  : the specified position
    @param direction : 1 of the 6 possible move directions, stored as tuple
    @param board     : current board's board
    @return          : boolean indicating whether SPREAD was successful or not
    """

    # Check first if position in dictionary/is a red piece
    if position not in board or board[position][0] == ENEMY:
        return False

    # also another safety protocol check if direction is valid
    if direction not in all_dir:
        return False

    # Since a valid position to use, store POWER
    curr_power = board[position][1]
    curr_pos = position

    # decrement power and each time place a piece in a new position
    while curr_power != 0:
        curr_pos = make_move(curr_pos, direction, board)
        curr_power -= 1

    # remove the entry from the current position
    del board[position]
    return True


def make_move(position: tuple, direction: tuple, board: dict[tuple, tuple]) -> tuple:
    """
    Returns the new position for iteration. Private function only called by SPREAD.

    @param position  : the specified position
    @param direction : 1 of the 6 possible move directions, stored as tuple
    @param board     : current board's board
    @return          : new position
    """

    # get new position
    tmp_pos = [INF, INF]
    for i in range(2):
        curr_pos = position[i] + direction[i]
        if curr_pos >= SIZE:
            tmp_pos[i] = curr_pos - SIZE
        elif curr_pos < 0:
            tmp_pos[i] = curr_pos + SIZE
        else:
            tmp_pos[i] = curr_pos
    new_pos = (tmp_pos[0], tmp_pos[1])

    # if the new position has already been occupied
    if new_pos in board:
        new_power = board[new_pos][1] + 1
        if new_power >= SIZE:
            del board[new_pos]
        else:
            board[new_pos] = (PLAYER, new_power)
    # otherwise, simply add spread player piece
    else:
        board[new_pos] = (PLAYER, 1)
    return new_pos


def check_loop(board: dict[tuple, tuple], position: tuple, direction: tuple) -> bool:
    # Assumes the board only has one red piece
    returned = position
    count = 0

    while True:
        print(render_board(board))
        spread(list(board.keys())[0], direction, board)
        count += 1
        if list(board.keys())[0] == returned:
            break

    print(render_board(board))
    print(f'From {position} in {direction}, took {count} spaces')
    return True
