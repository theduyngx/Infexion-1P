"""
    Authors : The Duy Nguyen (1100548) and Ramon Javier L. Felipe VI (1233281)
    Module  : a_star.py
    Purpose : Informed search using hybrid strategy of A* combining with greedy to find the optimal sequence
              of moves for a given input state of a board to reach its goal state.
"""

from state import *
from greedy_search import Greedy_search
from a_star import A_star


def informed_search(board: dict[tuple, tuple]) -> (int, [tuple]):
    """
    Informed search algorithm - hybrid algorithm using primarily A*, among other informed algorithms
    in special cases.

    @param board : the given board
    @return      : the number of generations required,
                   the optimal sequence of moves to reach goal state
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
