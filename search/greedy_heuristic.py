from .state import State, all_dir, MAX_VAL, PLAYER, ENEMY, SIZE
from .program import spread
from .a_star import enemy_filter, ally_filter

SPARSE = 20
INF = 9999

def h_greedy(state: State) -> list:
    return_list = []

    curr_board = state.board

    # We probably need to get both reds and blues anyway
    # Make sure to tag which set of pieces to use
    blues = enemy_filter(curr_board)
    reds = ally_filter(curr_board)
    
    if len(reds) >= len(blues):
        color = ENEMY
        curr_pieces = blues.keys()
        curr_target = reds.keys()
    else:
        color = PLAYER
        curr_pieces = reds.keys()
        curr_target = blues.keys()

    # Now after this, iterate through each piece and find
    # max number of pieces to eat
    adjacent_pieces = has_adjacent(curr_board, curr_pieces, curr_target)

    # I assume right now, the one eating up the heuristic is the number
    # of blues



    return return_list

def has_adjacent(board: dict[tuple, tuple], pieces: list, target: list) -> list:
    dict_dir = {}
    new_pieces = []
    
    for pos in pieces:
        if target == []:
            break
        x, y = pos
        tp, val = board[pos]

        # initialize the piece entry in direction dictionary
        for dir in all_dir:
            dict_dir[(x, y, dir)]  = []

        # for every other piece on the board - if player then player on direction
        for _pos in target:
            _x, _y = _pos
            _tp, _ = board[_pos]
            x_diff = x - _x
            y_diff = y - _y
            xd_abs = abs(x_diff)
            yd_abs = abs(y_diff)

            # x-direction
            if _x == x and _y != y:
                sign = int(y_diff / yd_abs)

                # add to both directions of x-direction if stack is sufficiently large
                if yd_abs <= val:
                    dict_dir[(x, y, (0, sign))].append(_pos)
                if yd_abs <= SIZE - val:
                    dict_dir[(x, y, (0, -sign))].append(_pos)

            # y-direction
            elif _x != x and _y == y:
                sign = int(x_diff / xd_abs)

                # add to both directions of y-direction if stack is sufficiently large
                if xd_abs <= val:
                    dict_dir[(x, y, (sign, 0))].append(_pos)
                if xd_abs <= SIZE - val:
                    dict_dir[(x, y, (-sign, 0))].append(_pos)

            # vertical direction
            elif _x != x:
                diff = abs(x_diff + y_diff)
                if xd_abs < yd_abs:
                    x_sign = 1
                    larger = yd_abs
                else:
                    x_sign = -1
                    larger = xd_abs
                y_sign = -x_sign

                # add to both directions of vertical direction if stack is sufficiently large
                if diff == 0 or diff == SIZE:
                    dict_dir[(x, y, (x_sign, y_sign))].append(_pos)
                    if larger <= val:
                        dict_dir[(x, y, (-x_sign, -y_sign))].append(_pos)

        # check the direction with most captures
        # CHANGED; instead of tracking max captures,
        # want to check if there were any captured
        max_captured = 0
        captured = []
        for dir in all_dir:
            curr_len = len(dict_dir[(x, y, dir)])
            if curr_len > 0:
                new_pieces.append(pos)
                break

    return new_pieces