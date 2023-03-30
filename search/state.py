MAX_VAL = 6
SIZE    = MAX_VAL + 1
PLAYER  = "r"
ENEMY   = "b"
x_dir   = [0, -1, -1, 0, 1, 1]
y_dir   = [1, 1, 0, -1, -1, 0]
all_dir = [(x_dir[i], y_dir[i]) for i in range(len(x_dir))]


# A structure representing state of board
class State:
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
        # if type(other) == int || type(other) == float:
        #     return self.g.
        return self.f_cost < other.f_cost

    def __eq__(self, other):
        return self.f_cost == other.f_cost
