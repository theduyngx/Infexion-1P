class State():
    def __init__(self, board: dict[tuple, tuple], moves: list) -> None:
        self.board = board
        self.moves = moves
        return
    
    # Adds new move
    def add_move(self, moves: list, move: tuple):
        self.moves.append(move)
        return
    
    def copy_state(self):
        new_state = State(self.board.copy(), self.moves)
        return new_state
