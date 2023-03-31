# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from a_star import A_star
from ids import *


def search(input: dict[tuple, tuple]) -> list[tuple]:
    """
    Main search function - using informed search A* algorithm to find optimal path.

    @param input : the input initial board
    @return      : sequence of optimal moves
    """
    return A_star(input)


def search_uninformed(board: dict[tuple, tuple]) -> list[tuple]:
    """
    Uninformed search algorithm finding the optimal sequence of moves for a given board to reach
    its goal state.

    @param board : given board
    @return      : sequence of optimal moves to reach goal state
    """

    # Here we're returning "hardcoded" actions for the given test.csv file.
    min_ret, _ = ids_score(board)
    return min_ret
