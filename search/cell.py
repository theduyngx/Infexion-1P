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


# A structure representing a cell occupied with a piece, which concerns the position and piece type
class Cell:
    def __init__(self, pos: (int, int), piece: (chr, int)):
        (x, y) = pos
        (tp, value) = piece
        self.x = x
        self.y = y
        self.type = tp

    def to_tuple(self):
        return self.x, self.y, self.type
