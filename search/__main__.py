# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

import heapq

from sys import stdin
from program import search, spread
from search.state import State
from utils import render_board
from test_boards import all_boards
from a_star import A_star
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
    print(render_board(board))
    print_sequence_board(board, A_star(board))
    return


def print_sequence_board(board: dict[tuple, tuple], sequence: list[tuple]):
    for x, y, dx, dy in sequence:
        spread((x, y), (dx, dy), board)
        print(render_board(board))


if __name__ == "__main__":
    st = time.time()
    names = ['test_case', 'suboptimal_kill', 'weight_problem', 'complex_1', 'complex_2', 'test_case_2', 'priority_fail']
    test(names[0])
    # d = {0: 1, 1: 1, 2: 1, 3: 0}
    # print(any(d.values()))

    # s1 = State(all_boards['complex_1'], [], 500)
    # s2 = State(all_boards['complex_2'], [1, 2, 3, 4], 200)
    # print(s1.board)
    # print(s2.board)
    # print(s1.__hash__())
    # print(s2.__hash__())

    # d = {2: [1, 2, 3, 4, 5], 1: [2, 5, 6, 7, 3, 2, 1], 3: [1, 5]}
    # s = list(map(lambda tup: tup[1], sorted(d.items(), key=lambda x: len(x[1]), reverse=True)))
    # s1 = list(map(lambda tup: (-len(tup[1]), tup[1]), d.items()))
    # print(s)
    # print(s1)
    # heapq.heapify(s1)
    # print(s1)

    et = time.time()
    print(f'TOTAL TIME TAKEN: {et-st}')
