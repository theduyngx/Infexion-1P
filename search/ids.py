"""
    Authors : The Duy Nguyen (1100548) and Ramon Javier L. Felipe VI (1233281)
    Module  : ids.py
    Purpose : Uninformed search algorithm IDS to find the optimal sequence of moves for a given input state
              of a board to reach its goal state.
"""

from movement import *


def DFS_limited(board: dict[tuple, tuple], depth: int, moves: list, valid: list) -> int:
    """
    Depth-first limited search algorithm used for IDS. Searching up till a certain specified depth.

    @param board : The provided board of the board
    @param depth : Depth threshold for DFS
    @param moves : sequence of moves
    @param valid : valid list (not sure what this is Raj?)
    @return      : the number of required generations
    """

    num_operations = 0

    if check_victory(board=board):
        valid.append((moves, depth, False))
        return num_operations

    elif depth <= 0:
        return num_operations

    for key in board.keys():
        for dir in all_dir:
            num_operations += 1
            diff_board = board.copy()
            check = spread(key, dir, board=diff_board)
            if check:
                moves.append((key[0], key[1], dir[0], dir[1]))
                curr_moves = moves.copy()
                num_operations += DFS_limited(diff_board, depth-1, curr_moves, valid)
                moves = moves[:-1]
    return num_operations


def IDS(board: dict[tuple, tuple]) -> (list[tuple], int):
    """
    IDS score of a given board.

    @param board : The provided board of the board
    @return      : The IDS score of a given board
    """
    num_operations = 0
    valid = [([], INF, True)]
    moves = []
    depth = 0
    while True:
        num_operations += DFS_limited(board, depth, moves, valid)
        if len(valid) > 1:
            sequence = valid[1][0]
            return sequence, num_operations
        moves = []
        depth += 1
