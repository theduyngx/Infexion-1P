from utils import render_board
from program import spread, makeMove

xCoords = [0, -1, -1, 0, 1, 1]
yCoords = [1, 1, 0, -1, -1, 0]

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
    print("OLD BOARD: ")
    print(render_board(board))
    # Put all possible edits here
    
    # currDir = (xCoords[0], yCoords[1])
    currDir = (xCoords[3], yCoords[3])

    # board, _ = spread((5,6), currDir, board)
    board, _ = spread((2,0), currDir, board)

    print("NEW BOARD: ")
    print(render_board(board))
    return

if __name__ == '__main__':
    main()