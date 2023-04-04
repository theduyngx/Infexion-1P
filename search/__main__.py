"""
    Authors : The Duy Nguyen (1100548) and Ramon Javier L. Felipe VI (1233281)
    Module  : __main__.py
    Purpose : Based on The University of Melbourne skeleton code - Project Part A: Single Player Infexion,
              COMP30024 Artificial Intelligence, Semester 1 2023. The main program.
"""

from program import search
from utils import render_board

from movement import spread
from test_boards import all_boards
import time


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


def print_sequence_board(board: dict[tuple, tuple], sequence: list[tuple], num_operations: int):
    """
    Print the different boards resulted from a sequence of moves.

    @param board          : the given board
    @param sequence       : sequence of moves
    @param num_operations : required number of generations to generate sequence
    @return               : none
    """
    print("")
    print("---------------------------------------------------")
    print("---------------- INITIAL STATE --------------------")
    print("---------------------------------------------------")
    print(render_board(board))
    print("\n")
    print("---------------------------------------------------")
    print("--------------------- MOVES -----------------------")
    print("---------------------------------------------------")
    for x, y, dx, dy in sequence:
        spread((x, y), (dx, dy), board)
        print(f"SPREAD ({x}, {y}) at direction ({dx}, {dy})\n")
        print(render_board(board))
        print("---------------------------------------------------")
    print("------------------ STATISTICS ---------------------")
    print("---------------------------------------------------")
    print(f"NUMBER OF MOVES: {len(sequence)}")
    print(f"NUMBER OF GENERATIONS: {num_operations}")


def test(name: str):
    """
    Test function calling main, and using the user-defined test cases specifically from
    test_boards.py

    @param name : name of test board
    @return     : the main function
    """
    board = all_boards[name]
    return main(board)


def main(board: dict[tuple, tuple]):
    """
    The main function that receives a board and creates a sequence of moves to reach the goal state.

    @param board : the given board
    @return      : none
    """
    num_operations, sequence = search(board)
    print_sequence_board(board, sequence, num_operations)
    return


if __name__ == "__main__":
    # timer
    st = time.time()

    # names of all test boards
    names = ['test_case', 'suboptimal_kill', 'weight_problem', 'test_case_2', 'priority_fail',
             'complex_1', 'complex_2', 'complex_3', 'sparse_1', 'sparse_2', 'sparse_ps', 'sparse_es',
             'all_1_48', 'all_12_37', 'all_23_26', 'all_37_12', 'all_43_5', 'all_2_1', 'all_2_2']

    # run test
    test('complex_3')
    et = time.time()
    print(f'TOTAL TIME TAKEN: {et-st}')
