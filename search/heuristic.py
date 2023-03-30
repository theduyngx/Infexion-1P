# Necessary Imports
import math
from state import *

# GLOBAL CONSTANTS
INF     = 9999


# Use this to identify the next possible move using euclidean spaces
def get_shortest_distance_1(board: dict[tuple, tuple]) -> tuple:
    # Need to get all the enemy pieces
    return_list = ()
    min_dist = float("inf")
    max_enemy = 0

    enemies = [item[0] for item in board.items() if item[1][0] == ENEMY]
    players = [item[0] for item in board.items() if item[1][0] == PLAYER]

    for p in players:
        # If the given player piece does end up being the ideal,
        # need to store the direction to move it in
        for e in enemies:
            for dir in all_dir:
                curr_dist, curr_enemy = get_heuristic(p, e, dir, board)
                if (curr_dist == min_dist and curr_enemy > max_enemy) or curr_dist < min_dist:
                    max_enemy = curr_enemy
                    min_dist = curr_dist
                    return_list = (p[0], p[1], dir[0], dir[1])
    return return_list


def get_shortest_priority(board: dict[tuple, tuple]) -> tuple:
    return_list = ()
    min_dist = float("inf")
    targeted_enemy = None

    enemies = [item[0] for item in board.items() if item[1][0] == ENEMY]
    players = [item[0] for item in board.items() if item[1][0] == PLAYER]

    # Create the enemy priority dictionary
    enemy_priority = make_enemy_priority(board)

    for p in players:
        for e in enemies:
            for dir in all_dir:
                curr_dist  = get_heuristic_priority(p, e, dir, board)
                if (curr_dist == min_dist and (enemy_priority[e] > enemy_priority[targeted_enemy]))\
                        or curr_dist < min_dist:
                    targeted_enemy = e
                    min_dist = curr_dist
                    return_list = (p[0], p[1], dir[0], dir[1])

    return return_list


# ---------------------- HEURISTIC FUNCTIONS ---------------------- #

def get_heuristic(player: tuple, enemy: tuple, dir: tuple, board: dict[tuple, tuple]) -> tuple:
    # Store the power of the current player piece
    curr_power = board[player][1]

    # Position the player piece to the farthest possible position after
    # it spreads to specified direction
    new_pos = add_direction(player, apply_scalar_dir(dir, curr_power))

    # Calculate the adjacent enemies and the enemy piece with the highest power
    adj_enemies, max_enemies = adjacent_enemies(board, player, dir)

    # Heuristic prioritizes any enemies that is within reach of the player piece in direction
    # If there are no enemy pieces within reach, just calculate the shortest distance to an enemy piece
    curr_dist = calc_distance(new_pos, enemy) - (2 * adj_enemies)
    return curr_dist, max_enemies


def get_heuristic_priority(player: tuple, enemy: tuple, dir: tuple, board: dict[tuple, tuple]) -> tuple:
    # Store the power of the current player piece
    curr_power = board[player][1]

    # Maybe get the minimum distance after a spread to a given enemy piece
    new_pos = player
    avg_distance = 0
    for _ in range(curr_power):
        new_pos = add_direction(new_pos, dir)
        curr_distance = calc_distance(new_pos, enemy)
        avg_distance += curr_distance
    return avg_distance/curr_power


# Tiebreaker function that returns total number of enemies present
# and the max POWER value of adjacent enemy pieces
def adjacent_enemies(board: dict[tuple, tuple], player: tuple, dir: tuple) -> tuple:
    curr_pow  = board[player][1]
    num_enemy = 0
    new_pos   = player
    max_num_enemy = 0
    for i in range(curr_pow):
        new_pos = add_direction(new_pos, dir)
        if new_pos in board and board[new_pos][0] == ENEMY:
            num_enemy += 1
            if 6 > board[new_pos][1] > max_num_enemy:
                max_num_enemy = board[new_pos][1]
    return num_enemy, max_num_enemy


# TEST: Want to know if using the potential of enemy instead works
def make_enemy_priority(board: dict[tuple, tuple]) -> dict[tuple, int]:
    priority_dict = {}
    # First collect all the enemies
    enemies = [item[0] for item in board.items() if item[1][0] == ENEMY]

    for enemy in enemies:
        # First keep the starting position
        # and a tracker for the max adjacent
        max_adjacent = 0
        new_pos      = enemy
        num_enemy    = 0
        enemy_pow    = board[enemy][1]
        for dir in all_dir:
            for _ in range(enemy_pow):
                new_pos = add_direction(new_pos, dir)
                # CONSIDER: Do we still add an enemy if enemy's power is 6?
                if new_pos in board and board[new_pos][0] == ENEMY:
                    # num_enemy += board[new_pos][1]
                    num_enemy += 1
            max_adjacent = max(max_adjacent, num_enemy)
            num_enemy = 0
        priority_dict[enemy] = max_adjacent
    return priority_dict


# Add and subtract coordinates in an INFLEXION board
def add_direction(a: tuple, b: tuple):
    tmp_pos = [INF, INF]
    for i in range(2):
        new_val = a[i] + b[i]
        if new_val > MAX_VAL:
            new_val = new_val - SIZE
        elif new_val < 0:
            new_val = SIZE + new_val
        tmp_pos[i] = new_val
    return tuple(tmp_pos)


# This function applies a scalar to the input
def apply_scalar_dir(a: tuple, scalar: int):
    new_tup = [INF, INF]
    for i in range(2):
        new_val = a[i]*scalar
        new_tup[i] = new_val
    return tuple(new_tup)


# CALCULATE DISTANCE BETWEEN 2 POINTS
def calc_distance(a: tuple, b: tuple) -> float:
    # First calculate the distances between the points
    tmp_pos = [INF, INF]
    for i in range(2):
        new_val = abs(a[i] - b[i])
        if new_val >= 4:
            new_val = SIZE - new_val
        tmp_pos[i] = new_val

    # Now get the euclidean distance
    return math.sqrt(tmp_pos[0]**2 + tmp_pos[1]**2)
