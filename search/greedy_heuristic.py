from .state import State, all_dir, MAX_VAL, PLAYER, ENEMY, SIZE
from .program import spread, check_victory
from .utils import render_board
# from .a_star import enemy_filter, ally_filter
import math

LOOP = 7
SPARSE = 20
INF = 9999

def h_greedy(state: State) -> list:
    curr_board = state.board
    sequence = []
    while not check_victory(curr_board):
        # First find the nearest red blue pair
        curr_move = get_shortest_distance(board=curr_board)
        sequence.append(curr_move)
        _ = spread((curr_move[0], curr_move[1]), (curr_move[2], curr_move[3]), curr_board)
        print(render_board(curr_board))
    print(sequence)
    return len(sequence)

# HELPER FUNCTIONS

def get_shortest_distance(board: dict[tuple, tuple]) -> tuple:
    # Need to get all the blue pieces
    
    # Return List/Tuple that stores [red_pos, blue_pos]
    return_list = ()
    min_dist = float("inf")

    blues = [item[0] for item in board.items() if item[1][0] == ENEMY]
    reds = [item[0] for item in board.items() if item[1][0] == PLAYER]

    adjacency = dict.fromkeys(blues, 0)
    adjacency = {k: adjacent_blues(board, k, blues) for k, _ in adjacency.items()}
    print(adjacency)

    for red in reds:
        # Store the current POWER of the red piece
        curr_power = board[red][1]

        # If the given red piece does end up being the ideal,
        # need to store the direction to move it in
        for blue in blues:
            for dir in all_dir:
                # THING IS: I don't know what the weighted value should be
                curr_adjacent = adjacency[blue]
                red_adjacent = adjacent_to_red(board, red, dir)
                curr_dist = avg_distance(red, blue, dir, curr_power) - max(curr_adjacent, red_adjacent)
                # print(f'{red}, {blue}, {dir} Distance: {curr_dist}')
                # curr_dist = calc_distance(new_pos, blue) 
                if curr_dist < min_dist:
                    # print(f'NEW DISTANCE: {curr_dist}')
                    min_dist = curr_dist
                    return_list = (red[0], red[1], dir[0], dir[1])
        
    return return_list

# CALCULATE AVERAGE DISTANCE
# Final scoring function to count adjacent blues
def adjacent_blues(board: dict[tuple, tuple], blue: tuple, all_blues: list) -> int:
    if len(all_blues) == 1 and all_blues[0] == blue or board[blue][1] >= 6:
        return 0

    tp, val = board[blue]
    x, y = blue
    max_captured = 0

    for dir in all_dir:
        curr_captured = 0
        new_pos = blue
        for _ in range(val):
            new_pos = add_direction(new_pos, dir)
            if new_pos in board and board[new_pos][0] == ENEMY and board[new_pos][1] < 6:
                curr_captured += 1
        max_captured = max(max_captured, curr_captured)
    return max_captured

def adjacent_to_red(board: dict[tuple, tuple], red: tuple, dir: tuple) -> int:
    blue_count = 0
    power = board[red][1]
    new_pos = red
    for _ in range(power):
        new_pos = add_direction(new_pos, dir)
        if new_pos in board and board[new_pos][0] == ENEMY:
            blue_count+=1
    return blue_count

def min_distance(from_pos: tuple, to_pos: tuple, dir: tuple, power: int) -> float:
    min_dist = float("inf")
    new_pos = from_pos
    for _ in range(power):
        new_pos = add_direction(new_pos, dir)
        min_dist = min(min_dist, calc_distance(new_pos, to_pos))
    return min_dist

def avg_distance(from_pos: tuple, to_pos:tuple, dir: tuple, power: int) -> float:
    avg_dist = 0
    new_pos = from_pos
    for i in range(power):
        new_pos = add_direction(new_pos, dir)
        avg_dist += calc_distance(new_pos, to_pos)
    return avg_dist/power

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

