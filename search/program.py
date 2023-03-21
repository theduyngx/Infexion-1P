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

def dfs_limited(state: dict[tuple, tuple], moves: list, root: tuple, depth: int) -> tuple:
# def dfs_limited(state: dict[tuple, tuple], root: tuple, depth: int) -> tuple:
# def dfs_limited(state: dict[tuple, tuple], root: tuple, depth: int) -> ([tuple], int, bool):
    """
    Depth-first limited search algorithm used for IDS. Searching up till a certain specified depth.

    Arguments:
    state -- The provided state of the board.
    root  -- Start position.
    depth -- Depth threshold for DFS.

    Output:
    a list of moves to reach to goal -> ({Current Position}, {Direction})
    a score that counts the number of spreads to reach goal,
    a boolean value indicating whether there may be any remaining child nodes yet to be traversed.
    """




    # HERE: get all possible move from a given root

    xCoords = [0, -1, -1, 0, 1, 1]
    yCoords = [1, 1, 0, -1, -1, 0]

    # Have to iterate through all the keys
    for key in state.keys():
        if state[key][0] == 'r':
            for i in range(len(xCoords)):
                newState, _ = makeMove(key, (xCoords[i], yCoords[i]), state)
                moves.append((key, (xCoords[i], yCoords[i])))
                return dfs_limited(newState, moves, )
                moves = moves[:-1]

    return (), INF, True

def RAJA_dfs_limited(state: dict[tuple, tuple], moves: list, depth: int) -> tuple:
    """
    Depth-first limited search algorithm used for IDS. Searching up till a certain specified depth.

    Arguments:
    state -- The provided state of the board.
    moves -- Recursively added onto or deleted until depth reached
    depth -- tracks how deep we are

    Output:
    a list of moves to reach to goal -> ({Current Position}, {Direction})
    a score that counts the number of spreads to reach goal,
    a boolean value indicating whether there may be any remaining child nodes yet to be traversed.
    """
    
    # Establish coordinates of directions
    xCoords = [0, -1, -1, 0, 1, 1]
    yCoords = [1, 1, 0, -1, -1, 0]

    for key in state.keys():
        if state[key][0] == 'r':
            for i in range(len(xCoords)):
                newState, _ = makeMove(key, (xCoords[i], yCoords[i]), state)
                moves.append((key, (xCoords[i], yCoords[i])))
                dfs_limited(newState, moves, )
                moves = moves[:-1]

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

# ----------------------------------------------------------------------- RAJA: HELPER FUNCTIONS -----------------------------------------------------------------------

# Main function to move pieces
# For now returns state and a boolean indicating if it was updated
def spread(position: tuple, direction:tuple, state: dict[tuple, tuple]) -> tuple:
    # Check first if position in dictionary/is a red piece
    if state[position][0] == 'b' or not position in state:
        return state, False
    
    # Since a valid position to use, store POWER
    currPower = state[position][1]
    currPos = position

    # Place a piece in each new position
    while currPower != 0:
        state, currPos = makeMove(currPos, direction, state)
        currPower-=1
    
    # Last thing to do is remove the entry from the current posiion
    del state[position]

    # Now we want to move all the piecs from the stack to positions
    # in the corresponding direction
    return state, True

# Returns the new position for iteration
def makeMove(position: tuple, direction: tuple, state: dict[tuple, tuple]) -> tuple:
    newPos = []
    for i in range(len(position)):
        currPos = position[i] + direction[i]
        if 0 <= currPos <= 6:
            newPos.append(currPos)
        elif currPos == 7:
            newPos.append(0)
        elif currPos == -1:
            newPos.append(6)
    # Now check if there needs to be adjutment on the specific tile
    newPos = (newPos[0], newPos[1])

    if newPos in state:
        newPower = state[newPos][1] + 1

        # Here we want to remove the key from the board
        if newPower > 6:
            del state[newPos]
        # Just increment power for used position
        else:
            state[newPos] = ('r', newPower)
    
    # Since this is new, can just add a single red piece
    else:
        state[newPos] = ('r', 1)

    # Make sure to return the new position for the loop
    return state, newPos


# Test victory condition
def checkVictory(state: dict[tuple, tuple]) -> bool:
    for key in state.keys():
        if state[key][0] == 'b':
            return False
    return True
