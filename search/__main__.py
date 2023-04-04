"""
    Authors : The Duy Nguyen (1100548) and Ramon Javier L. Felipe VI (1233281)
    Module  : __main__.py
    Purpose : Based on The University of Melbourne skeleton code - Project Part A: Single Player Infexion,
              COMP30024 Artificial Intelligence, Semester 1 2023. The main program.
"""

from typing import Callable
import time

from program import *
from test_boards import all_boards
from utils import *


def parse_input(input: str) -> dict[tuple, tuple]:
    """
    Parse input CSV into a dictionary of board cell states.

    @param input : the input string as the parsed csv file
    @return      : the initial board state
    """
    return {
        (int(r), int(q)): (p.strip(), int(k))
        for r, q, p, k in [
            line.split(',') for line in input.splitlines()
            if len(line.strip()) > 0
        ]
    }


def test(name: str, search_f: Callable[[dict[tuple, tuple]], tuple]):
    """
    Test function calling main, and using the user-defined test cases specifically from
    test_boards.py

    @param name     : name of test board
    @param search_f : the search function
    @return         : the main function
    """
    board = all_boards[name]
    return main(board, search_f)


def main(board: dict[tuple, tuple], search_f: Callable[[dict[tuple, tuple]], tuple]):
    """
    The main function that receives a board and creates a sequence of moves to reach the goal state.

    @param search_f : the search function
    @param board    : the given board
    """
    start = time.time()
    sequence, num_operations, func_name = search_f(board)
    end = time.time()
    time_taken = end - start
    display_name = get_algorithm_name(func_name)
    print_sequence_board(board, sequence, num_operations, display_name, time_taken)
    return


if __name__ == "__main__":
    # names of all test boards
    names = ['test_case', 'suboptimal_kill', 'weight_problem', 'test_case_2', 'priority_fail',
             'complex_1', 'complex_2', 'complex_3', 'sparse_1', 'sparse_2', 'sparse_ps', 'sparse_es',
             'all_1_48', 'all_12_37', 'all_23_26', 'all_37_12', 'all_43_5', 'all_2_1', 'all_2_2']

    # run test
    test('all_1_48', search_f=search_informed)
