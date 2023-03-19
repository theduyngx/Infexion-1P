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


def get_all_nodes(state: dict[tuple, tuple], root: tuple) -> [tuple]:
    (_, val) = state[root]
    # HERE: is where we define where the piece can move and how that affects the state
    # Note: We should also think about whether the list of tuples would include positions where the
    #       piece gets populated to as well, or only the initial piece next to it
    return []


def dfs_limited(state: dict[tuple, tuple], root: tuple, depth: int) -> ([tuple], int, bool):
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
    # 2 approaches to attempt movement from root:
    #   1. After every single hypothetical move, we create the exact copy of the state with changes
    #      resulting from the move
    #   2. We create a roll_back function where after a move, we revert to the previous state
    return (), INF, True


def ids_score(state: dict[tuple, tuple], root: tuple) -> (int, [tuple]):
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
