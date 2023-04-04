"""
    Author  : The Duy Nguyen
    Module  : sequence.py
    Purpose : object representing a sequence of moves that reach a goal state, which includes other attributes
              such as what algorithm produces such a sequence, its memory use and number of operations.
"""


class Sequence:
    """
    A structure representing a sequence of moves to reach goal state
    moves     - sequence of moves, represented by a list of positions
    num_ops   - the number of operations required to produce the sequence
    mem_use   - memory requirement
    algo_name - name of algorithm that produces the sequence in question
    """
    def __init__(self, moves: list[tuple], num_ops: int, mem_use: int, algo_name: str):
        self.moves     = moves
        self.num_ops   = num_ops
        self.mem_use   = mem_use
        self.algo_name = algo_name
