# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from utils import render_board

# constants
SIZE = 7
MAX_PTS = SIZE ** 2
INF = 9999
PLAYER = 'r'
ENEMY = 'b'

x_dir = [0, -1, -1, 0, 1, 1]
y_dir = [1, 1, 0, -1, -1, 0]
all_dir = [(x_dir[i], y_dir[i]) for i in range(len(x_dir))]


def get_all_roots(state: dict[tuple, tuple]) -> list[tuple]:
    """
    Get all roots that player can start with, given only SPREAD action is permitted.

    Arguments:
    state -- The provided state of the board.

    Output:
    a list of (x, y) positions of all possible start move (root).
    """
    all_roots = []
    total_score = 0
    for x, y in state.keys():
        value = state[(x, y)]
        total_score += value[1]
        if value[0] == PLAYER:
            all_roots.append((x, y))
    if total_score > MAX_PTS or total_score <= 0:
        return []
    return all_roots

def dfs_limited(state: dict[tuple, tuple], root: tuple, depth: int) -> tuple:
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

    # HERE: get all possible move from a given root

    # x_coords = [0, -1, -1, 0, 1, 1]
    # y_coords = [1, 1, 0, -1, -1, 0]

    return [], INF, True

def ids_score(state: dict[tuple, tuple], root: tuple) -> tuple:
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
    depth = 0
    while True:
        found, score, finished = dfs_limited(state, root, depth)
        if found:
            return found, score
        elif finished:
            return [], INF
        depth += 1


def search(state: dict[tuple, tuple]) -> list[tuple]:
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
    print(render_board(state, ansi=False))

    # CODE
    # get all moves
    all_roots = get_all_roots(state)
    min_score = INF
    min_ret = []
    for root in all_roots:
        # Do IDS (or informed searching algorithm) to get the min score of each possible root
        # Get the min score and from that get ret (the best play to win)
        score, ret = ids_score(state, root)
        if score < min_score:
            min_score = score
            min_ret = ret

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