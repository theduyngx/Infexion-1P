"""
    Authors : The Duy Nguyen (1100548) and Ramon Javier L. Felipe VI (1233281)
    Module  : ids.py
    Purpose : Uninformed search algorithm IDS to find the optimal sequence of moves for a given input state
              of a board to reach its goal state.
"""

from movement import *
from sequence import Sequence


def DFS_limited(board: dict[tuple, tuple], depth: int, moves: list, valid: list) -> (int, int):
    """
    Depth-first limited search algorithm used for IDS. Searching up till a certain specified depth.
    Time complexity is O(b^d), but space complexity is only O(d) since we use recursion; meaning we
    need not care about other branches at any given point.

    @param board : The provided board of the board
    @param depth : Depth threshold for DFS
    @param moves : sequence of moves
    @param valid : valid list
    @return      : the number of required generations, and the memory usage
    """

    num_ops = 0
    mem_use = 0

    # goal state
    if check_victory(board=board):
        valid.append((moves, depth, False))
        return num_ops, mem_use

    # reached limited depth
    elif depth <= 0:
        return num_ops, mem_use

    prev_mem_brd = 0  # previous memory of the copied board, flushed after finishing a branch
    prev_mem_dir = 0  # previous memory getting flushed after visiting each branch

    # for each branch of a given board
    for key in board.keys():
        for dir in all_dir:
            diff_board = board.copy()
            check = spread(key, dir, board=diff_board)

            # we update number of operation (state generation) + updating memory
            num_ops += 1
            mem_use -= prev_mem_brd
            mem_use -= prev_mem_dir
            prev_mem_brd = 0
            prev_mem_dir = 0
            mem_use += len(diff_board)
            prev_mem_brd += len(diff_board)

            if check:
                moves.append((key[0], key[1], dir[0], dir[1]))
                curr_moves = moves.copy()

                # this is going down further to the next branch
                curr_ops, curr_mem = DFS_limited(diff_board, depth-1, curr_moves, valid)
                num_ops      += curr_ops
                mem_use      += len(curr_moves) + curr_mem
                prev_mem_dir += len(curr_moves) + curr_mem

                # cut-off when goal state reached, or move back by 1 level and keep going
                if len(valid) > 1:
                    return num_ops, mem_use
                moves = moves[:-1]
    return num_ops, mem_use


def IDS(board: dict[tuple, tuple]) -> Sequence:
    """
    IDS score of a given board.

    @param board : The provided board of the board
    @return      : object sequence representing the optimal sequence of moves
    """
    num_ops  = 0
    mem_use  = 0
    prev_mem = 0

    valid = [([], INF, True)]
    moves = []
    depth = 0
    while True:
        mem_use -= prev_mem
        curr_ops, curr_mem = DFS_limited(board, depth, moves, valid)
        num_ops += curr_ops
        mem_use += curr_mem
        prev_mem = curr_mem
        if len(valid) > 1:
            sequence = Sequence(valid[1][0], num_ops, mem_use, IDS.__name__)
            return sequence
        moves = []
        depth += 1
