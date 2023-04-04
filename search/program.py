"""
    Authors : The Duy Nguyen (1100548) and Ramon Javier L. Felipe VI (1233281)
    Module  : program.py
    Purpose : The program with 2 different search strategies - informed and uninformed.
"""

from state import *
from ids import IDS
from greedy_search import Greedy_search
from a_star import A_star


def search_informed(board: dict[tuple, tuple]) -> ([tuple], int, str):
    """
    Informed search algorithm - hybrid algorithm using primarily A*, among other informed algorithms
    in special cases.

    @param board : the given board
    @return      : the optimal sequence of moves to reach goal state,
                   the number of generations required,
                   the search algorithm name
    """
    all_1 = (len(board) == TOTAL)
    if not all_1 and len(board) >= DENSE:
        for pos in board:
            tp, val = board[pos]
            if tp == ENEMY and val != MIN_VAL:
                all_1 = False
                break
            all_1 = True
    func = Greedy_search if all_1 else A_star
    sequence, num_operations = func(board)
    return sequence, num_operations, func.__name__


def search_uninformed(board: dict[tuple, tuple]) -> (list[tuple], int, str):
    """
    Uninformed search algorithm finding the optimal sequence of moves for a given board to reach
    its goal state.

    @param board : given board
    @return      : the sequence of optimal moves to reach goal state,
                   the number of generations required,
                   the search algorithm name
    """
    sequence, num_operations = IDS(board)
    return sequence, num_operations, IDS.__name__
