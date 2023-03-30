# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from .utils import render_board
from .heuristic import get_shortest_not_greedy, get_shortest_priority, get_shortest_distance_1
import math
# from .dist_calculator import get_shortest_distance_1

# constants
SIZE = 7
# MAX_PTS = SIZE ** 2
INF = 9999
PLAYER = 'r'
ENEMY = 'b'
x_dir = [0, -1, -1, 0, 1, 1]
y_dir = [1, 1, 0, -1, -1, 0]
all_dir = [(x_dir[i], y_dir[i]) for i in range(len(x_dir))]

def search(input: dict[tuple, tuple]) -> list[tuple]:
    sequence = []
    while not check_victory(input):
        # First find the nearest red blue pair
        # curr_move = get_shortest_distance_2(board=board)
        curr_move = get_shortest_distance_1(board=input)
        # curr_move = get_shortest_not_greedy(board=input) 

        # nearest_dir = get_shortest_direction(board, nearest_red, nearest_blue)
        sequence.append(curr_move)
        _ = spread((curr_move[0], curr_move[1]), (curr_move[2], curr_move[3]), input)
        print(render_board(input))
    return sequence

def search_priority(input: dict[tuple, tuple]) -> list[tuple]:
    sequence = []
    while not check_victory(input):
        # First find the nearest red blue pair
        # curr_move = get_shortest_distance_2(board=board)
        # curr_move = get_shortest_priority(board=input)
        curr_move = get_shortest_not_greedy(board=input)

        # nearest_dir = get_shortest_direction(board, nearest_red, nearest_blue)
        sequence.append(curr_move)
        _ = spread((curr_move[0], curr_move[1]), (curr_move[2], curr_move[3]), input)
        print(render_board(input))
    return sequence


def search_2(input: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """

    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    # print(render_board(input, ansi=False))

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    min_ret, depth = ids_score(state=input)

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    return min_ret

# RAJA: HELPER FUNCTIONS
# For now returns state and a boolean indicating if it was updated
def spread(position: tuple, direction: tuple, state: dict[tuple, tuple]) -> bool:
    """
    SPREAD movement for a specified piece.

    Arguments:
    position -- the specified position.
    direction -- 1 of the 6 possible move directions, stored as tuple
    state -- current board's state.

    Output:
    boolean indicating whether SPREAD was successful or not
    """

    # Check first if position in dictionary/is a red piece
    if position not in state or state[position][0] == ENEMY:
        # check1 = position not in state
        # check2 = state[position][0] == ENEMY
        # print(f'Move in {position} to {direction} NOT VALID because either:\nPosition not in state: {check1}\nUsing enemy {check2}')
        return False

    # also another safety protocol check if direction is valid
    if direction not in all_dir:
        return False

    # Since a valid position to use, store POWER
    curr_power = state[position][1]
    curr_pos = position

    # decrement power and each time place a piece in a new position
    while curr_power != 0:
        curr_pos = make_move(curr_pos, direction, state)
        curr_power -= 1

    # remove the entry from the current position
    del state[position]
    return True


# HELPER FUNCTIONS FOR THE MOVEMENT
def make_move(position: tuple, direction: tuple, state: dict[tuple, tuple]) -> tuple:
    """
    Returns the new position for iteration. Private function only called by SPREAD.

    Arguments:
    position -- the specified position.
    direction -- 1 of the 6 possible move directions, stored as tuple
    state -- current board's state.

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
    if new_pos in state:
        new_power = state[new_pos][1] + 1
        if new_power >= SIZE:
            del state[new_pos]
        else:
            state[new_pos] = (PLAYER, new_power)
    # otherwise, simply add spread player piece
    else:
        state[new_pos] = (PLAYER, 1)
    
    return new_pos


def check_victory(state: dict[tuple, tuple]) -> bool:
    """
    Goal test - whether player has spread to all blue pieces.
    """
    return ENEMY not in map(lambda tup: tup[0], state.values())

# MOVES: list of tuples containing position and direction
def dfs_limited(state: dict[tuple, tuple], depth: int, moves: list, valid: list):
# def RAJA_dfs_limited(state: dict[tuple, tuple], depth: int, moves: list) -> tuple:
# def dfs_limited(state: dict[tuple, tuple], root: tuple, depth: int) -> ([tuple], int, bool):
    """
    Depth-first limited search algorithm used for IDS. Searching up till a certain specified depth.

    Arguments:
    state -- The provided state of the board.
    root  -- Start position.
    depth -- Depth threshold for DFS.

    Output:
    a list of moves to reach to goal,
    a score that counts the number of steps to reach goal,
    a boolean value indicating whether there may be any remaining child nodes yet to be traversed.
    """

    # print(all_dir)

    # HERE: get all possible move from a given root

    # x_coords = [0, -1, -1, 0, 1, 1]
    # y_coords = [1, 1, 0, -1, -1, 0]

    if check_victory(state=state):
        # print(f'VICTORY: {moves}')
        # print('VICTORY')
        # print(f'DEPTH: {depth}, MOVE LEN: {len(moves)}')
        # print("WIN STATE")
        # print(f'MOVES: {moves}')
        # print(render_board(state))
        valid.append((moves, depth, False))
        return
        # return depth, False
    
    elif depth <= 0:
        # if (moves[0] == ((5,6), (-1, 1)) and moves[1] == ((3,1),(0,1)) and moves[2] == ((3,2),(-1,1))):
            # print(f'LOSE: {moves}')
            # print('LOSE')
            # print(f'DEPTH: {depth}, MOVE LEN: {len(moves)}')
            # print(render_board(state)
        #     pass
        # print(render_board(state))
        # print(render_board(state))
        # return INF, True
        return

    for key in state.keys():
        for dir in all_dir:
            diff_state = state.copy()
            check = spread(key, dir, state=diff_state)
            if check:
                moves.append((key[0], key[1], dir[0], dir[1]))
                currMoves = moves.copy()
                dfs_limited(diff_state, depth-1, currMoves, valid)
                moves = moves[:-1]
    return

def ids_score(state: dict[tuple, tuple]) -> tuple:
# def ids_score(state: dict[tuple, tuple], root: tuple) -> ([tuple], int):
    """
    Depth-first limited search algorithm used for IDS. Searching up till a certain specified depth.

    Arguments:
    state -- The provided state of the board.
    root  -- Start position.

    Output:
    list of optimal moves to reach to goal (given specified root)
    and the additive score (number of said moves)
    """
    # tracker = (INF, True)
    valid = [([], INF, True)]
    moveList = []
    depth = 0
    while True:
        # print(f'--------------------------------------------------------------------------------CURRENT DEPTH: {depth}-----------------------------------------------------------------------------')
        dfs_limited(state, depth, moveList, valid=valid)
        # print(f'Current Score: {score}, Current Finished: {finished}')
        if len(valid) > 1:
            return valid[1][0], valid[1][1]
        # elif finished:
        #    return [], INF
        moveList=[]
        depth += 1


def RAJA_search(state: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary of cell states, where
    the keys are tuples of (r, q) coordinates, and the values are tuples of (p, k) cell states. The
    output should be a list of  actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    Arguments:
    state -- Board's initial state.

    Output:
    the list of positions representing optimal moves
    """

    # The render_board function is useful for debugging -- it will print out a board state in a
    # human-readable format. Try changing the ansi argument to True to see a colour-coded version
    # (if your terminal supports it).
    # print(render_board(state, ansi=False))

    # CODE
    # get all moves
    # all_roots = get_all_roots(state)
    
    min_ret, depth = ids_score(state=state)

    print(f'Current Sequence: {min_ret}')

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    return min_ret[0] # [('b', 1, -1, 0)]

# ---------------------------------------------------------------------------------------------------------------------- HELPER FUNCTIONS TO THEORYCRAFT ----------------------------------------------------------------------------------------------------------------------

def check_loop(board: dict[tuple, tuple], position: tuple, direction: tuple) -> bool:
    # Assumes the board only has one red piece
    returned = position
    count = 0

    while True:
        print(render_board(board))
        spread(list(board.keys())[0], direction, board)
        # print(f'Num Spaces: {count}')
        count+=1
        if list(board.keys())[0] == returned:
            break
    
    print(render_board(board))

    print(f'From {position} in {direction}, took {count} spaces')

    return True


