from utils import render_board
from program import spread, check_victory


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
    print(render_board(board, ansi=True))

    directions = [(0, -1), (0, -1), (0, -1), (-1, 0), (0, 1), (1, 0)]
    positions  = [(2,  0), (2,  6), (2,  5), (2,  0), (1, 0), (2, 2)]
    for i in range(len(directions)):
        curr_dir = directions[i]
        curr_pos = positions[i]
        _ = spread(curr_pos, curr_dir, board)
        print("MOVE " + str(i+1) + ": ")
        print("Victory status: " + str(check_victory(board)))
        print(render_board(board, ansi=True))

    ret = spread((0, 6), (0, 1), board)
    print("\nPiece NOT existing hence ret for SPREAD is " + str(ret))
    ret = spread((5, 6), (1, 0), board)
    print("Piece existing hence ret for SPREAD is " + str(ret))
    print(render_board(board, ansi=True))


if __name__ == '__main__':
    main()
