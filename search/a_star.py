from board import *


# heuristic function
def h(state: dict[tuple, tuple]) -> float:
    num_enemy = get_num_enemy(state)
    return num_enemy
