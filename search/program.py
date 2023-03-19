# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from utils import render_board

# constants
SIZE = 7
MAX_PTS = SIZE ** 2
INF = 9999


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
        if value[0] == 'r':
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

    # xCoords = [0, -1, -1, 0, 1, 1]
    # yCoords = [1, 1, 0, -1, -1, 0]

    return (), INF, True


def ids_score(state: dict[tuple, tuple], root: tuple) -> tuple:
    # def ids_score(state: dict[tuple, tuple], root: tuple) -> (int, [tuple]):
    """
    Depth-first limited search algorithm used for IDS. Searching up till a certain specified depth.
    Arguments:
    state -- The provided state of the board.
    root  -- Start position.
    Output:
    the score, and a list of optimal moves to reach to goal (given specified root)
    """
    depth = 0
    while True:
        found, score, finished = dfs_limited(state, root, depth)
        if found:
            return found, score
        elif finished:
            return INF, ()
        depth += 1


def search(state: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary of cell states, where
    the keys are tuples of (r, q) coordinates, and the values are tuples of (p, k) cell states. The
    output should be a list of  actions, where each action is a tuple of (r, q, dr, dq) coordinates.
    See the specification document for more details.
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
# Main function to move pieces
# For now returns state and a boolean indicating if it was updated
def spread(position: tuple, direction: tuple, state: dict[tuple, tuple]) -> tuple:
    # Check first if position in dictionary/is a red piece
    if state[position][0] == 'b' or position not in state:
        return state, False

    # Since a valid position to use, store POWER
    curr_power = state[position][1]
    curr_pos = position

    # Now decrement power and each time place
    # a piece in a new position
    while curr_power != 0:
        state, curr_pos = make_move(curr_pos, direction, state)
        curr_power -= 1

    # Last thing to do is remove the entry from the current position
    del state[position]

    # Now we want to move all the pieces from the stack to positions
    # in the corresponding direction
    return state, True


# Returns the new position for iteration
def make_move(position: tuple, direction: tuple, state: dict[tuple, tuple]) -> tuple:
    new_pos = []
    for i in range(len(position)):
        curr_pos = position[i] + direction[i]
        if 0 <= curr_pos <= 6:
            new_pos.append(curr_pos)
        elif curr_pos == 7:
            new_pos.append(0)
        elif curr_pos == -1:
            new_pos.append(6)
    # Now check if there needs to be adjustment on the specific tile
    new_pos = (new_pos[0], new_pos[1])

    if new_pos in state:
        new_power = state[new_pos][1] + 1

        # Here we want to remove the key from the board
        if new_power > 6:
            del state[new_pos]
        # Just increment power for used position
        else:
            state[new_pos] = ('r', new_power)

    # Since this is new, can just add a single red piece
    else:
        state[new_pos] = ('r', 1)

    # Make sure to return the new position for the loop
    return state, new_pos


# Test victory condition
def check_victory(state: dict[tuple, tuple]) -> bool:
    for key in state.keys():
        if state[key][0] == 'b':
            return False
    return True
