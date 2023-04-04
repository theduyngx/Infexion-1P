"""
    Authors : The Duy Nguyen (1100548) and Ramon Javier L. Felipe VI (1233281)
    Module  : program.py
    Purpose : The program with 2 different search strategies - informed and uninformed.
"""

from state import *
from sequence import Sequence
from ids import IDS
from greedy_search import Greedy_search
from a_star import A_star


def search_informed(board: dict[tuple, tuple]) -> Sequence:
    """
    Informed search algorithm - hybrid algorithm using primarily A*, among other informed algorithms
    in special cases.

    @param board : the given board
    @return      : object sequence, representing the optimal sequence of moves
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
        return Greedy_search(board)
    return A_star(board)


def search_uninformed(board: dict[tuple, tuple]) -> Sequence:
    """
    Uninformed search algorithm finding the optimal sequence of moves for a given board to reach
    its goal state.

    @param board : given board
    @return      : object sequence, representing the optimal sequence of moves
    """
    return IDS(board)
