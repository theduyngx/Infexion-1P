# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

import heapq
from sys import stdin
import time
from .program import search, spread
from .state import State
from .utils import render_board
from .test_boards import all_boards, make_dense_board, make_dense_board_random, make_dense_board_blue, make_alternating_board, make_ratio_board
from .a_star import A_star, greedy_blue, greedy_red, enemy_filter, ally_filter
from .greedy_heuristic import h_greedy

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
    sequence, new_time = A_star(board)
    print_sequence_board(board, sequence)
    print(f'SEQUENCE: {sequence}, TIME: {new_time}')
    return

def test_density(red_start: tuple):
    for i in range(1, 50):
        st = time.time()
        # curr_board = make_dense_board(1, 6, red_start, i)
        curr_board = make_dense_board_blue(1, 1, red_start, i)
        print(render_board(curr_board))
        sequence, total_time = A_star(curr_board)
        # print_sequence_board(curr_board, sequence)
        et = time.time()
        total_time = min(total_time, et-st)

        print(f'CURRENT NUM: {i},\nSEQUENCE: {sequence}')
        print(f'TIME TAKEN: {total_time}')
    return

def test_density_random(red_start: tuple):
    for i in range(1, 50):
        st = time.time()
        curr_board = make_dense_board_random(1, red_start, i)
        print(render_board(curr_board))
        sequence, total_time = A_star(curr_board)
        # print_sequence_board(curr_board, sequence)
        et = time.time()
        total_time = min(total_time, et-st)

        print(f'CURRENT NUM: {i},\nSEQUENCE: {sequence}')
        print(f'TIME TAKEN: {total_time}')
    return

def test_alternating():
    for i in range(1, 50):
        st = time.time()
        # curr_board = make_dense_board(1, 6, red_start, i)
        curr_board = make_alternating_board(i)
        print(render_board(curr_board))
        sequence, total_time = A_star(curr_board)
        # print_sequence_board(curr_board, sequence)
        et = time.time()
        total_time = min(total_time, et-st)
        print(f'CURRENT NUM: {i},\nSEQUENCE: {sequence}')
        print(f'TIME TAKEN: {total_time}') 
    return

def test_ratio(count):
    for i in range(count+1, 50):
        st = time.time()
        curr_board = make_ratio_board(count, i)
        print(render_board(curr_board))
        sequence, total_time = A_star(curr_board)
        et = time.time()
        total_time = min(total_time, et-st)
        print(f'CURRENT NUM: {i},\nSEQUENCE: {sequence}')
        print(f'TIME TAKEN: {total_time}') 
    return

def test_h_greedy(board):
    test_state = State(board, [], 0)
    print(render_board(board))
    num_moves = h_greedy(test_state)
    print(f'Num Moves: {num_moves}')
    return


def print_sequence_board(board: dict[tuple, tuple], sequence: list[tuple]):
    for x, y, dx, dy in sequence:
        spread((x, y), (dx, dy), board)
        print(render_board(board))
    return

def test_reduce_red(board: dict[tuple, tuple]):
    sequence, curr_time = [], float("inf")
    eats = 0
    print(render_board(board))

    while curr_time >= 30:
        print(f'CURRENT EATS: {eats}')
        print(render_board(board))
        board = greedy_blue(test_board)
        sequence, curr_time = A_star(board)
        print(f'Time Taken: {curr_time}, Eats: {eats}')
        eats += 1

    print(render_board(board))
    print(f'EATS TAKEN: {eats}')
    num_blues = len(enemy_filter(board))
    num_reds = len(ally_filter(board))
    print(f'NUM BLUES: {num_blues}, NUM REDS: {num_reds}')
    print(f'TIME TAKEN: {curr_time}')
    return

def test_reduce_blu(board: dict[tuple, tuple]):
    sequence, curr_time = [], float("inf")
    eats = 0
    print(render_board(board))

    while curr_time >= 30:
        print(f'CURRENT EATS: {eats}')
        print(render_board(board))
        board = greedy_red(test_board)
        sequence, curr_time = A_star(board)
        print(f'Time Taken: {curr_time}, Eats: {eats}')
        eats += 1

    print(render_board(board))
    print(f'EATS TAKEN: {eats}')
    num_blues = len(enemy_filter(board))
    num_reds = len(ally_filter(board))
    print(f'NUM BLUES: {num_blues}, NUM REDS: {num_reds}')
    print(f'TIME TAKEN: {curr_time}')
    return


if __name__ == "__main__":
    st = time.time()
    names = ['test_case', 'suboptimal_kill', 'weight_problem', 'complex_1', 'complex_2', 'complex_3',
             'sparse_1', 'sparse_2', 'sparse_ps', 'sparse_es',
             'test_case_2', 'priority_fail', 'dense_1', 'fully_dense']
    # TEST FOR DENSITY WITH 1 PIECES
    # test_density((3,3))
    # test_alternating()
    # test_ratio(40)
    test_board = all_boards['all_1_48'].copy()
    # test('complex_1')
    # test_h_greedy(test_board)
    # print(render_board(test_board))
    # test_board = greedy_red(test_board)
    # test_board = greedy_blue(test_board)
    # print(render_board(test_board))

    test_reduce_blu(test_board)

    # TEST FOR DENSITY WITH RANDOM NUMBER OF POWER VALUES
    # EDIT test_boards function to control power values
    # test_density_random((0,0))
    et = time.time()
    print(f'TOTAL TIME TAKEN: {et-st}')
