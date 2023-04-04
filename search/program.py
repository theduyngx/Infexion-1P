"""
    Authors : The Duy Nguyen (1100548) and Ramon Javier L. Felipe VI (1233281)
    Module  : program.py
    Purpose : Based on The University of Melbourne skeleton code - Project Part A: Single Player Infexion,
              COMP30024 Artificial Intelligence, Semester 1 2023. Includes the search functions for finding
              the optimal paths to reach goal state.
"""

from informed_search import informed_search
from ids import IDS


def search(input: dict[tuple, tuple]) -> (int, list[tuple]):
    """
    Main search function - using informed search A* algorithm to find optimal path.

    @param input : the input initial board
    @return      : sequence of optimal moves
    """
    return informed_search(input)


def search_uninformed(board: dict[tuple, tuple]) -> (int, list[tuple]):
    """
    Uninformed search algorithm finding the optimal sequence of moves for a given board to reach
    its goal state.

    @param board : given board
    @return      : sequence of optimal moves to reach goal state
    """

    # Here we're returning "hardcoded" actions for the given test.csv file.
    num_operations, min_ret = IDS(board)
    return num_operations, min_ret
