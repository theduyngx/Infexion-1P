# IMPORTS
import queue
import heapq
from program import check_victory, spread
from state import *


def A_star(board: dict[tuple, tuple]) -> [tuple]:
    """
    A* algorithm to find the optimal sequence of moves to reach goal state

    @param board : the provided board (initial state)
    @return      : the sequence of optimal moves
    """
    min_found  = queue.PriorityQueue()	# discovered nodes
    g_cost     = {}		                # real cumulative cost from root
    f_cost     = {}		                # best guess f = g + h
    discovered = {}

    curr_state = State(board, [], 0)
    hash_curr  = curr_state.__hash__()
    min_found.put(curr_state)		    # init state has now been discovered
    discovered[hash_curr] = 1
    g_cost[hash_curr]     = 0
    f_cost[hash_curr]     = 0
    # min_moves = []
    # num_moves = INF

    while not min_found.empty():
        curr_state = min_found.get()
        hash_curr  = curr_state.__hash__()
        del discovered[hash_curr]
        if check_victory(curr_state.board):
            return curr_state.moves
            # return the optimal moves to reach the goal state
            # if len(curr_state.moves) < num_moves:
            #     min_moves = curr_state.moves
            #     num_moves = len(curr_state.moves)

        for neighbor in get_neighbors(curr_state):
            x, y, dir_x, dir_y = neighbor
            new_state = State.copy_state(curr_state)
            new_state.add_move(neighbor)
            _ = spread(position=(x, y), direction=(dir_x, dir_y), board=new_state.board)
            hash_new = new_state.__hash__()
            # true cost from init to new_state via curr_state
            g_cost_accum = g_cost[hash_curr] + 1

            if hash_new not in g_cost or g_cost_accum < g_cost[hash_new]:
                g_cost[hash_new] = g_cost_accum
                f_cost[hash_new] = g_cost_accum + h(new_state)
                new_state.f_cost = f_cost[hash_new]
                if hash_new not in discovered:
                    discovered[hash_new] = 1
                    min_found.put(new_state)
    return []


def h(state: State) -> int:
    """
    Heuristic function.
    """
    return h2(state)


def h2(state: State) -> int:
    """
    Heuristic function method 2.
    """

    # algorithm
    # search for the single direction with the most blue pieces, +1 move
    # then ignore them and find the next direction with most blue pieces without the ones just checked earlier
    # do this until we have accounted for every blue piece
    # for each of these directions, we +1 number of moves

    # after this (could be initially expensive but on the long run will be cheaper), we check if any of our red
    # pieces are on any of the previous direction; if not then +1 again

    # --> h = number of directions (from dir with most blue to least) + (red on any direction == TRUE)

    board = state.board
    spreaded   = {}
    dict_dir   = {}
    for pos in board:
        x, y = pos
        tp, val = board[pos]
        if tp == PLAYER:
            continue

        # initialize the piece entry in direction dictionary
        dict_dir[(x, y, (1, 0))]  = []
        dict_dir[(x, y, (0, 1))]  = []
        dict_dir[(x, y, (1, -1))] = []

        for _pos in board:
            _x, _y = _pos
            _tp, _val = board[_pos]
            if _tp == PLAYER:
                continue

            # x-direction
            if _x == x and _y != y:
                dict_dir[(x, y, (1, 0))].append(_pos)

            # y-direction
            elif _x != x and _y != y:
                dict_dir[(x, y, (0, 1))].append(_pos)

            # vertical direction
            else:
                x_diff = x - _x
                y_diff = y - _y
                diff = abs(x_diff + y_diff)
                if diff == 0 or diff == SIZE:
                    dict_dir[(x, y, (1, -1))].append(_pos)

        # delete empty entries
        if not dict_dir[(x, y, (1, 0))]:
            del dict_dir[(x, y, (1, 0))]
        if not dict_dir[(x, y, (0, 1))]:
            del dict_dir[(x, y, (0, 1))]
        if not dict_dir[(x, y, (1, -1))]:
            del dict_dir[(x, y, (1, -1))]

    # then sort the direction dictionary by direction with the highest number of blue pieces
    dir_sort = list(map(lambda tup: (-len(tup[1]), tup[1]), dict_dir.items()))

    # due to it being min-heap (no max heap in python3), we push in negative lengths
    heapq.heapify(dir_sort)
    num_moves = 0
    while dir_sort:
        entry = heapq.heappop(dir_sort)
        update_list = []
        neg_len, pieces = entry
        for piece in pieces:
            if piece in spreaded:
                continue
            update_list.append(piece)
        if len(update_list) == -neg_len:
            # do it again ig
            for piece in pieces:
                spreaded[piece] = 1
                num_moves += 1
        elif update_list:
            update_entry = (-len(update_list), update_list)
            heapq.heappush(dir_sort, update_entry)

    return num_moves


def get_neighbors(state: State) -> [tuple]:
    neighbors = []
    board = state.board
    for x, y in board.keys():
        p_type, stack = board[(x, y)]
        if p_type == ENEMY:
            continue
        for dir_x, dir_y in all_dir:
            neighbors.append((x, y, dir_x, dir_y))
    return neighbors
