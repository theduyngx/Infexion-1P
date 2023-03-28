from .program import spread, check_victory
from.utils import render_board
import math

INF = 9999
LOOP = 7
MAX_VAL = 6
BLUE = 'b'
RED = 'r'
x_dir = [0, -1, -1, 0, 1, 1]
y_dir = [1, 1, 0, -1, -1, 0]
all_dir = [(x_dir[i], y_dir[i]) for i in range(len(x_dir))]

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
    # First calculate the distances betweenn the points
    tmp_pos = [INF, INF]
    for i in range(2):
        new_val = abs(a[i] - b[i])
        if new_val >= 4:
            new_val = LOOP - new_val
        tmp_pos[i] = new_val
    
    # Now get the euclidean distance
    return math.sqrt(tmp_pos[0]**2 + tmp_pos[1]**2)

# USES AVERAGE, NOT WORKING FOR SOME REASON
def get_shortest_distance_2(board: dict[tuple, tuple]) -> tuple:
    # Need to get all the blue pieces
    
    # Return List/Tuple that stores [red_pos, blue_pos]
    # return_list = ()
    min_avg = float("inf")

    blues = [item[0] for item in board.items() if item[1][0] == BLUE]
    blue_count = len(blues)
    reds = [item[0] for item in board.items() if item[1][0] == RED]
    use_red = None
    red_min_dir = None

    for red in reds:
        # Store the current POWER of the red piece
        curr_power = board[red][1]
        min_dir_dist = float("inf")
        avg_dist = 0
        red_curr_dir = None

        # If the given red piece does end up being the ideal,
        # need to store the direction to move it in

        for blue in blues:
            curr_dist = 0
            min_dist = float("inf")
            curr_min_dir = None
            for dir in all_dir:
                new_pos = add_direction(red, apply_scalar_dir(dir, curr_power))
                # new_pos = add_direction(red, dir)
                # curr_blues = adjacent_blues(board, red, dir)
                # curr_dist = calc_distance(new_pos, blue) - curr_blues - (curr_power-1)
                curr_dist = calc_distance(new_pos, blue) 
                if curr_dist < min_dist:
                    min_dist = curr_dist
                    # return_list = (red[0], red[1], dir[0], dir[1])
                    curr_min_dir = dir
            
            # Now check if the direction leads to the shortest distance
            if min_dist < min_dir_dist:
                min_dir_dist = min_dist
                red_curr_dir = curr_min_dir
    
            # Add to the average of the distances
            avg_dist += min_dist

        # Check if the average distance between blues is minimum        
        avg_dist = avg_dist/blue_count
        if avg_dist < min_avg:
            min_avg = avg_dist
            use_red = red
            red_min_dir = red_curr_dir
        
    return (use_red[0], use_red[1], red_min_dir[0], red_min_dir[1])

# HEURISTIC FUNCTION
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

def get_shortest_distance_1(board: dict[tuple, tuple]) -> tuple:
    # Need to get all the blue pieces
    
    # Return List/Tuple that stores [red_pos, blue_pos]
    return_list = ()
    min_dist = float("inf")
    max_blue = 0

    blues = [item[0] for item in board.items() if item[1][0] == BLUE]
    reds = [item[0] for item in board.items() if item[1][0] == RED]

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

# Final scoring function to count adjacent blues
def adjacent_blues(board: dict[tuple, tuple], red: tuple, dir: tuple) -> tuple:
    curr_pow = board[red][1]
    blue_count = 0
    new_pos = red
    max_blue = 0
    for i in range(curr_pow):
        new_pos = add_direction(new_pos, dir)
        if new_pos in board and board[new_pos][0] == BLUE:
            # blue_count += board[new_pos][1]
            blue_count += 1
            if board[new_pos][1] < 6 and board[new_pos][1] > max_blue:
                max_blue = board[new_pos][1]
    # print(f'RED: {red}, POWER: {board[red][1]}, DIR: {dir} -> {blue_count}')
    return blue_count, max_blue

# Compare minimum values that are the same
def compare_min(board: dict[tuple, tuple], red_a: tuple, red_b: tuple) -> tuple:
    return

"""
# This function adds the direction from a given point
def get_shortest_direction(board: dict[tuple, tuple], red_piece: tuple, blue_piece: tuple) -> tuple:
    min_dist = float("inf")
    return_dir = None
    red_pow = board[red_piece][1]
    for dir in all_dir:
        # Get the point where the spread reaches the farthest
        # and check if it's close to the closest blue piece
        new_pos = add_direction(red_piece, apply_scalar_dir(dir, red_pow))
        curr_dist = calc_distance(new_pos, blue_piece)
        if curr_dist < min_dist:
            min_dist = curr_dist
            return_dir = dir
    return return_dir
"""


def a_star_euc(board: dict[tuple, tuple]) -> list:
    sequence = []
    while not check_victory(board):
        # First find the nearest red blue pair
        # curr_move = get_shortest_distance_2(board=board)
        curr_move = get_shortest_distance_1(board=board)
        # nearest_dir = get_shortest_direction(board, nearest_red, nearest_blue)
        sequence.append(curr_move)
        _ = spread((curr_move[0], curr_move[1]), (curr_move[2], curr_move[3]), board)
        print(render_board(board))
    return sequence

# ---------------------------------------------------------------------------------------------------------------------- HELPER FUNCTIONS TO THEORYCRAFT ----------------------------------------------------------------------------------------------------------------------

def check_loop(board: dict[tuple, tuple], position: tuple, direction: tuple) -> bool:
    # Assumes the board only has one red piece
    returned = position
    count = 0

    while True:
        print(render_board(board))
        spread(list(board.keys())[0], direction, board)
        # print(f'Num Spaces: {count}')
        count+=1
        if list(board.keys())[0] == returned:
            break
    
    print(render_board(board))

    print(f'From {position} in {direction}, took {count} spaces')

    return True

