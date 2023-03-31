# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from .utils import render_board
# from .state import *
from .state import State, all_dir, MAX_VAL, PLAYER, ENEMY, SIZE
from .heuristic import get_shortest_priority, get_shortest_distance_1

# constants
INF = 9999


def search(input: dict[tuple, tuple]) -> list[tuple]:
    sequence = []
    while not check_victory(input):
        # First find the nearest red blue pair
        curr_move = get_shortest_distance_1(board=input)
        sequence.append(curr_move)
        _ = spread((curr_move[0], curr_move[1]), (curr_move[2], curr_move[3]), input)
        print(render_board(input))
    return sequence


def search_priority(input: dict[tuple, tuple]) -> list[tuple]:
    sequence = []
    while not check_victory(input):
        # First find the nearest red blue pair
        # curr_move = get_shortest_distance_2(board=board)
        curr_move = get_shortest_priority(board=input)

        # nearest_dir = get_shortest_direction(board, nearest_red, nearest_blue)
        sequence.append(curr_move)
        _ = spread((curr_move[0], curr_move[1]), (curr_move[2], curr_move[3]), input)
        print(render_board(input))
    return sequence


def search_2(input: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell boards, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell boards. The output should be a list of
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    min_ret, depth = ids_score(board=input)
    return min_ret


# RAJA: HELPER FUNCTIONS
# For now returns board and a boolean indicating if it was updated
def spread(position: tuple, direction: tuple, board: dict[tuple, tuple]) -> bool:
    """
    SPREAD movement for a specified piece.

    Arguments:
    position -- the specified position.
    direction -- 1 of the 6 possible move directions, stored as tuple
    board -- current board's board.

    Output:
    boolean indicating whether SPREAD was successful or not
    """

    # Check first if position in dictionary/is a red piece
    if position not in board or board[position][0] == ENEMY:
        return False

    # also another safety protocol check if direction is valid
    if direction not in all_dir:
        return False

    # Since a valid position to use, store POWER
    curr_power = board[position][1]
    curr_pos = position

    # decrement power and each time place a piece in a new position
    while curr_power != 0:
        curr_pos = make_move(curr_pos, direction, board)
        curr_power -= 1

    # remove the entry from the current position
    del board[position]
    return True


# HELPER FUNCTIONS FOR THE MOVEMENT
def make_move(position: tuple, direction: tuple, board: dict[tuple, tuple]) -> tuple:
    """
    Returns the new position for iteration. Private function only called by SPREAD.

    Arguments:
    position -- the specified position.
    direction -- 1 of the 6 possible move directions, stored as tuple
    board -- current board's board.

    Output:
    new position
    """

    # get new position
    tmp_pos = [INF, INF]
    for i in range(2):
        curr_pos = position[i] + direction[i]
        if curr_pos >= SIZE:
            tmp_pos[i] = curr_pos - SIZE
        elif curr_pos < 0:
            tmp_pos[i] = curr_pos + SIZE
        else:
            tmp_pos[i] = curr_pos
    new_pos = (tmp_pos[0], tmp_pos[1])

    # if the new position has already been occupied
    if new_pos in board:
        new_power = board[new_pos][1] + 1
        if new_power >= SIZE:
            del board[new_pos]
        else:
            board[new_pos] = (PLAYER, new_power)
    # otherwise, simply add spread player piece
    else:
        board[new_pos] = (PLAYER, 1)
    return new_pos


def check_victory(board: dict[tuple, tuple]) -> bool:
    """
    Goal test - whether player has spread to all blue pieces.
    """
    return ENEMY not in map(lambda tup: tup[0], board.values())


# MOVES: list of tuples containing position and direction
def dfs_limited(board: dict[tuple, tuple], depth: int, moves: list, valid: list):
    """
    Depth-first limited search algorithm used for IDS. Searching up till a certain specified depth.

    Arguments:
    board -- The provided board of the board.
    root  -- Start position.
    depth -- Depth threshold for DFS.

    Output:
    a list of moves to reach to goal,
    a score that counts the number of steps to reach goal,
    a boolean value indicating whether there may be any remaining child nodes yet to be traversed.
    """

    if check_victory(board=board):
        valid.append((moves, depth, False))
        return

    elif depth <= 0:
        return

    for key in board.keys():
        for dir in all_dir:
            diff_board = board.copy()
            check = spread(key, dir, board=diff_board)
            if check:
                moves.append((key[0], key[1], dir[0], dir[1]))
                curr_moves = moves.copy()
                dfs_limited(diff_board, depth-1, curr_moves, valid)
                moves = moves[:-1]
    return


def ids_score(board: dict[tuple, tuple]) -> tuple:
    """
    Depth-first limited search algorithm used for IDS. Searching up till a certain specified depth.

    Arguments:
    board -- The provided board of the board.
    root  -- Start position.

    Output:
    list of optimal moves to reach to goal (given specified root)
    and the additive score (number of said moves)
    """
    # tracker = (INF, True)
    valid = [([], INF, True)]
    moves = []
    depth = 0
    while True:
        dfs_limited(board, depth, moves, valid=valid)
        if len(valid) > 1:
            return valid[1][0], valid[1][1]
        # elif finished:
        #    return [], INF
        moves = []
        depth += 1


def RAJA_search(board: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary of cell boards, where
    the keys are tuples of (r, q) coordinates, and the values are tuples of (p, k) cell boards. The
    output should be a list of  actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    Arguments:
    board -- Board's initial board.

    Output:
    the list of positions representing optimal moves
    """

    min_ret, depth = ids_score(board=board)
    print(f'Current Sequence: {min_ret}')

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    return min_ret[0] # [('b', 1, -1, 0)]


def check_loop(board: dict[tuple, tuple], position: tuple, direction: tuple) -> bool:
    # Assumes the board only has one red piece
    returned = position
    count = 0

    while True:
        print(render_board(board))
        spread(list(board.keys())[0], direction, board)
        # print(f'Num Spaces: {count}')
        count += 1
        if list(board.keys())[0] == returned:
            break

    print(render_board(board))
    print(f'From {position} in {direction}, took {count} spaces')
    return True
