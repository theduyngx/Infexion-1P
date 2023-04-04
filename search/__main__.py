# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from sys import stdin
from program import search
from utils import render_board

from movement import spread
from test_boards import all_boards
import time

# WARNING: Do *not* modify any of the code in this file, and submit it as is!
#          You should be modifying the search function in program.py instead.
#
# The code here is used by the autograder to feed your solution input and parse
# the resulting action sequence. Failed test cases due to modification of this
# file will not receive any marks.
#
# Notice that output is printed to stdout, and all actions are prepended with
# the word "SPREAD". This is to enable the autograder to distinguish between
# the final action sequence and any other output that may be printed to stdout.
# Regardless, you must not print anything to stdout in your *final* submission.


def parse_input(input: str) -> dict[tuple, tuple]:
    """
    Parse input CSV into a dictionary of board cell states.
    """
    return {
        (int(r), int(q)): (p.strip(), int(k))
        for r, q, p, k in [
            line.split(',') for line in input.splitlines()
            if len(line.strip()) > 0
        ]
    }


def print_sequence(sequence: list[tuple]):
    """
    Print the given action sequence. All actions are prepended with the
    word "SPREAD", and each action is printed on a new line.
    """
    for r, q, dr, dq in sequence:
        print(f"SPREAD {r} {q} {dr} {dq}")


def main():
    """
    Main entry point for program.
    """
    input = parse_input(stdin.read())
    sequence: list[tuple] = search(input)
    print_sequence(sequence)


def test(name: str):
    board = all_boards[name]
    print("\n")
    print("---------------------------------------------------")
    print("---------------- INITIAL STATE --------------------")
    print("---------------------------------------------------")
    print(render_board(board))
    print_sequence_board(board, search(board))
    return


def print_sequence_board(board: dict[tuple, tuple], sequence: list[tuple]):
    print("\n")
    print("---------------------------------------------------")
    print("--------------------- MOVES -----------------------")
    print("---------------------------------------------------")
    for x, y, dx, dy in sequence:
        spread((x, y), (dx, dy), board)
        print(f"SPREAD ({x}, {y}) at direction ({dx}, {dy})\n")
        print(render_board(board))
        print("---------------------------------------------------")
    print(f"NUMBER OF MOVES: {len(sequence)}")


if __name__ == "__main__":
    st = time.time()
    names = ['test_case', 'suboptimal_kill', 'weight_problem', 'test_case_2', 'priority_fail',
             'complex_1', 'complex_2', 'complex_3', 'sparse_1', 'sparse_2', 'sparse_ps', 'sparse_es',
             'all_1_48', 'all_12_37', 'all_23_26', 'all_37_12', 'all_43_5', 'all_2_1', 'all_2_2']
    test('complex_2')
    et = time.time()
    print(f'TOTAL TIME TAKEN: {et-st}')
