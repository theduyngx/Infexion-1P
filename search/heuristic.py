# Necessary Imports
import math

# GLOBAL CONSTANTS
INF = 9999
MAX_VAL = 6
LOOP = MAX_VAL + 1
PLAYER = 'r'
ENEMY = 'b'
x_dir = [0, -1, -1, 0, 1, 1]
y_dir = [1, 1, 0, -1, -1, 0]
all_dir = [(x_dir[i], y_dir[i]) for i in range(len(x_dir))]

# ----------------------------------------------- SEARCH FUNCTION FOR MOST DESIRABLE PATH ----------------------------------------------

# Use this to identify the next possible move using euclidean spaces
def get_shortest_distance_1(board: dict[tuple, tuple]) -> tuple:
    # Need to get all the blue pieces
    
    # Return List/Tuple that stores [red_pos, blue_pos]
    return_list = ()
    min_dist = float("inf")
    max_blue = 0

    blues = [item[0] for item in board.items() if item[1][0] == ENEMY]
    reds = [item[0] for item in board.items() if item[1][0] == PLAYER]

    for red in reds:
        # If the given red piece does end up being the ideal,
        # need to store the direction to move it in
        for blue in blues:
            curr_dist = 0
            for dir in all_dir:
                curr_dist, curr_blue = get_heuristic(red, blue, dir, board)
                if (curr_dist == min_dist and curr_blue > max_blue) or curr_dist < min_dist:
                    max_blue = curr_blue
                    min_dist = curr_dist
                    return_list = (red[0], red[1], dir[0], dir[1])
        
    return return_list

def get_shortest_not_greedy(board: dict[tuple, tuple]) -> tuple:
    # Return List/Tuple that stores [red_pos, blue_pos]
    return_list = ()
    min_dist = float("inf")
    max_blue = 0

    blues = [item[0] for item in board.items() if item[1][0] == ENEMY]
    reds = [item[0] for item in board.items() if item[1][0] == PLAYER]

    for red in reds:
        # If the given red piece does end up being the ideal,
        # need to store the direction to move it in
        for blue in blues:
            curr_dist = 0
            for dir in all_dir:
                curr_dist, _ = get_heuristic(red, blue, dir, board)
                if curr_dist < min_dist:
                    min_dist = curr_dist
                    return_list = (red[0], red[1], dir[0], dir[1])
        
    return return_list

def get_shortest_priority(board: dict[tuple, tuple]) -> tuple:
    return_list = ()

    min_dist = float("inf")
    targeted_blue = None

    blues = [item[0] for item in board.items() if item[1][0] == ENEMY]
    reds = [item[0] for item in board.items() if item[1][0] == PLAYER]

    # Create the blue priority dictionary
    blue_priority = make_blue_priority(board)

    for red in reds:
        for blue in blues:
            for dir in all_dir:
                curr_dist  = get_heuristic_priority(red, blue, dir, board)
                if (curr_dist == min_dist and (blue_priority[blue] > blue_priority[targeted_blue])) or curr_dist < min_dist:
                    targeted_blue = blue
                    min_dist = curr_dist
                    return_list = (red[0], red[1], dir[0], dir[1])

    return return_list

# ----------------------------------------------- HEURISTIC FUNCTIONS ----------------------------------------------

def get_heuristic(red: tuple, blue: tuple, dir: tuple, board: dict[tuple, tuple]) -> tuple:
    # Store the power of the current red piece
    curr_power = board[red][1]
    
    # Position the red piece to the farthest possible position after
    # it spreads to specified direction
    new_pos = add_direction(red, apply_scalar_dir(dir, curr_power))

    # Calculate the adjacent blues and the blue piece with the highest power
    adj_blues, max_blue = adjacent_blues(board, red, dir)

    # Heuristic prioritizes any blues that is within reach of the red piece in direction
    # If there are no blue pieces within reach, just calculate the shortest distance to a blue piece
    curr_dist = calc_distance(new_pos, blue) - (2*adj_blues)
    return curr_dist, max_blue

def get_heuristic_priority(red: tuple, blue: tuple, dir: tuple, board: dict[tuple, tuple]) -> tuple:
    # Store the power of the current red piece
    curr_power = board[red][1]

    # Maybe get the minimum distance after a spread to a given blue piece
    new_pos = red
    curr_distance = 0
    avg_distance = 0
    for _ in range(curr_power):
        new_pos = add_direction(new_pos, dir)
        curr_distance = calc_distance(new_pos, blue)
        avg_distance += curr_distance
    return avg_distance/curr_power


# ----------------------------------------------- HELPER FUNCTIONS FOR HEURISTIC CALCULATIONS ----------------------------------------------

# Tiebreaker function that returns total number of blues present
# and the max POWER value of adjacent blue pieces
def adjacent_blues(board: dict[tuple, tuple], red: tuple, dir: tuple) -> tuple:
    curr_pow = board[red][1]
    blue_count = 0
    new_pos = red
    max_blue = 0
    for i in range(curr_pow):
        new_pos = add_direction(new_pos, dir)
        if new_pos in board and board[new_pos][0] == ENEMY:
            # blue_count += board[new_pos][1]
            blue_count += 1
            if board[new_pos][1] < 6 and board[new_pos][1] > max_blue:
                max_blue = board[new_pos][1]
    # print(f'RED: {red}, POWER: {board[red][1]}, DIR: {dir} -> {blue_count}')
    return blue_count, max_blue

# TEST: Want to know if using the potential of blue instead works
def make_blue_priority(board: dict[tuple, tuple]) -> dict[tuple, int]:
    priority_dict = {}

    # First collect all the blues
    blues = [item[0] for item in board.items() if item[1][0] == ENEMY]

    for blue in blues:
        # First keep the starting position
        # and a tracker for the max adjacent
        max_adjacent = 0
        new_pos = blue
        blue_count = 0
        blue_pow = board[blue][1]
        for dir in all_dir:
            for _ in range(blue_pow):
                new_pos = add_direction(new_pos, dir)
                # CONSIDER: Do we still add a blue if blue's power is 6?
                if new_pos in board and board[new_pos][0] == ENEMY:
                    # blue_count += board[new_pos][1]
                    blue_count += 1
            max_adjacent = max(max_adjacent, blue_count)
            blue_count = 0
        priority_dict[blue] = max_adjacent
    return priority_dict

# ----------------------------------------------- HELPER FUNCTIONS FOR BOARD CALCULATIONS ----------------------------------------------- 

# Add and subtract coordinates in an INFLEXION board
def add_direction(a: tuple, b:tuple):
    tmp_pos = [INF, INF]
    for i in range(2):
        new_val = a[i] + b[i]
        if new_val > MAX_VAL:
            new_val = new_val - LOOP
        elif new_val < 0:
            new_val = LOOP + new_val
        tmp_pos[i] = new_val
    return tuple(tmp_pos)

# This function applies a scalar to the input
def apply_scalar_dir(a:tuple, scalar:int):
    new_tup = [INF, INF]
    for i in range(2):
        new_val = a[i]*scalar
        new_tup[i] = new_val
    return tuple(new_tup)


# CALCULATE DISTANCE BETWEEN 2 POINTS
def calc_distance(a: tuple, b: tuple):
    # First calculate the distances between the points
    tmp_pos = [INF, INF]
    for i in range(2):
        new_val = abs(a[i] - b[i])
        if new_val >= 4:
            new_val = LOOP - new_val
        tmp_pos[i] = new_val
    
    # Now get the euclidean distance
    return math.sqrt(tmp_pos[0]**2 + tmp_pos[1]**2)