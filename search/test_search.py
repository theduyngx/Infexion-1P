import time
import os
# from . import program
from program import check_victory, spread, RAJA_dfs_limited
# from . import utils
from dist_calculator import check_loop

print(f'CUURR PATH: {os.getcwd()}')

INF = 9999

def main():
    board = {
        (5, 6): ("r", 2),
        (1, 0): ("b", 2),
        (1, 1): ("b", 1),
        (3, 2): ("b", 1),
        (1, 3): ("b", 3),
        (2, 0): ("r", 3),
        (2, 4): ("b", 6),
        (2, 5): ("b", 3)
    }
    print("\nINIT: ")
    print("Victory status: " + str(check_victory(board)))
    # print(render_board(board))

    directions = [(0, -1), (0, -1), (0, -1), (-1, 0), (0, 1), (1, 0)]
    positions  = [(2,  0), (2,  6), (2,  5), (2,  0), (1, 0), (2, 2)]
    for i in range(len(directions)):
        curr_dir = directions[i]
        curr_pos = positions[i]
        _ = spread(curr_pos, curr_dir, board)
        print("MOVE " + str(i+1) + ": ")
        print("Victory status: " + str(check_victory(board)))
        # print(render_board(board))

    ret = spread((0, 6), (0, 1), board)
    print("\nPiece NOT existing hence ret for SPREAD is " + str(ret))
    print("Piece existing hence ret for SPREAD is " + str(ret))
    # print(render_board(board))

    # ------------------- testing ------------------- #
    d = {'a': (1, 2), 'b': (3, 4), 'c': (5, 6)}
    print(1 in map(lambda tup: tup[0], d.values()))
    if 'd' not in d or d['z'][0] != 1:
        print("Lazy!")

# RAJA: TESTS IDS IMPLEMENTATION
def main2():
    st = time.time()
    board = {
        (5, 6): ("r", 2),
        (1, 0): ("b", 2),
        (1, 1): ("b", 1),
        (3, 2): ("b", 1),
        (1, 3): ("b", 3)
    }

    """
    board = {
        (4, 0): ("r", 1),
        (1, 0): ("b", 2),
        (1, 1): ("b", 1),
        (1, 3): ("r", 4),
        (2 ,3): ("r", 1)
    }
    """

    # movesList = []
    # valid = [([], INF, True)]
    # tracker = (INF, True)

    print(search(board))

    # print(RAJA_dfs_limited(board, 1, movesList, valid=valid))
    # print(valid)
    et = time.time()
    print(f'Time Taken: {et-st}')
    return

def main3():
    x_dir = [0, -1, -1, 0, 1, 1]
    y_dir = [1, 1, 0, -1, -1, 0]
    all_dir = [(x_dir[i], y_dir[i]) for i in range(len(x_dir))]
    board = {
        (5, 6): ("r", 2)
    }
    print(check_loop(board, (5, 6), (0, -1)))
    return

if __name__ == '__main__':
    # main()
    # main2()
    main3()
