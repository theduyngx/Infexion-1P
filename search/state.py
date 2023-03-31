"""
    Authors : The Duy Nguyen (1100548) and Ramon Javier L. Felipe VI (1233281)
    File    : ids.py
    Purpose : Including functions directly related to the board, as well as other global constants of a board
              and the class State, which includes the board itself and other metadata.
"""

INF     = 9999
MAX_VAL = 6
SIZE    = MAX_VAL + 1
PLAYER  = "r"
ENEMY   = "b"
x_dir   = [0, -1, -1, 0, 1, 1]
y_dir   = [1, 1, 0, -1, -1, 0]
all_dir = [(x_dir[i], y_dir[i]) for i in range(len(x_dir))]


# A structure representing state of board
class State:
    """
    A structure representing state of board, including these attributes:
    board  - the current 'state' of the board
    moves  - the list of moves for the initial board to reach to current state
    f_cost - sum of the accumulated real (g) cost and the estimated (h) cost to reach to goal state
    """
    def __init__(self, board: dict[tuple, tuple], moves: list, f_cost: float):
        self.board  = board
        self.moves  = moves
        self.f_cost = f_cost

    # Adds new move
    def add_move(self, move: tuple):
        self.moves.append(move)

    # copy state
    def copy_state(self):
        new_state = State(self.board.copy(), self.moves.copy(), self.f_cost)
        return new_state

    # hashable object
    def __hash__(self):
        return hash(frozenset(self.board.items()))

    # comparison operator
    def __lt__(self, other):
        return self.f_cost < other.f_cost

    def __eq__(self, other):
        return self.f_cost == other.f_cost


def check_victory(board: dict[tuple, tuple]) -> bool:
    """
    Goal test - whether player has spread to all blue pieces.

    @param board : the given board
    @return      : boolean indicating if board is goal state
    """
    return ENEMY not in map(lambda tup: tup[0], board.values())
