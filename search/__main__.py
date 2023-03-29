# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from sys import stdin
from .program import search
from .heuristic import calc_distance
# from .dist_calculator import check_loop, a_star_euc
from .utils import render_board
from .test_boards import all_boards
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

def main3():
    x_dir = [0, -1, -1, 0, 1, 1]
    y_dir = [1, 1, 0, -1, -1, 0]
    all_dir = [(x_dir[i], y_dir[i]) for i in range(len(x_dir))]
    board = {
        (5, 6): ("r", 1)
    }
    # for dir in all_dir:
    dir = all_dir[4]
    # print(check_loop(board, (5, 6), dir))
    return

def a_star_test():
    board = {
        (5, 6): ("r", 2),
        (1, 0): ("b", 2),
        (1, 1): ("b", 1),
        (3, 2): ("b", 1),
        (1, 3): ("b", 3)
    }

    print(render_board(board))
    sequence = search(board)
    print(sequence)
    return


def main4():
    board = {
        # (2,2): ("r", 3),
        # (2,1): ("b", 1),
        # (2,0): ("b", 1),
        # (3,6): ("r", 1),
        (4,4): ("r", 1),
        (4,5): ("r", 1),
        (5,4): ("b", 3),
        (5,3): ("b", 4),
        (5,2): ("b", 1),
        (5,1): ("b", 6)
        
    }

    print(render_board(board))
    sequence = search(board)
    print(sequence)
    return

def distance_test_func():
    actual = 1
    board = all_boards['distance_test_1']
    print(f'Underestimated Distance: {calc_distance(list(board.keys())[0], list(board.keys())[1])}')
    print(f'Actual Distance: {actual}')

    return

if __name__ == "__main__":
    st = time.time()

    # main()
    # main3()
    a_star_test()
    # main4()
    # distance_test_func()
    
    et = time.time()
    print(f'TOTAL TIME TAKEN: {et-st}')
