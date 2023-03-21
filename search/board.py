PLAYER  = "r"
ENEMY   = "b"


# A structure representing a position
class Position:
    def __init__(self, tup: tuple):
        (x, y) = tup
        self.x = x
        self.y = y

    def to_tuple(self):
        return self.x, self.y


# A structure representing a piece
class Piece:
    def __init__(self, tup: (str, int)):
        (tp, value) = tup
        self.type = tp
        self.value = value

    def to_tuple(self):
        return self.type, self.value


# A structure representing a cell occupied by a piece, which concerns the position and piece type
class Cell:
    def __init__(self, pos: (int, int), piece: (chr, int)):
        (x, y) = pos
        (tp, value) = piece
        self.x = x
        self.y = y
        self.type = tp

    def to_tuple(self):
        return self.x, self.y, self.type


# function to get the total number of enemies currently in state
def get_num_enemy(state: dict[tuple, tuple]) -> int:
    return sum(map(lambda piece: piece[0] == ENEMY, state.values()))
