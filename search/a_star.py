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
    min_found = queue.PriorityQueue()  # discovered nodes
    g_cost = {}  # real cumulative cost from root
    f_cost = {}  # best guess f = g + h
    discovered = {}

    curr_state = State(board, [], 0)
    hash_curr = curr_state.__hash__()
    min_found.put(curr_state)  # init state has now been discovered
    discovered[hash_curr] = 1
    g_cost[hash_curr] = 0
    f_cost[hash_curr] = 0
    # min_moves = []
    # num_moves = INF

    while not min_found.empty():
        curr_state = min_found.get()
        hash_curr = curr_state.__hash__()
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
    The heuristic function.

    @param state : given current state
    @return      : the heuristic of said state (estimated number of moves to goal)
    """
    return h2(state)


def h2(state: State) -> int:
    """
    Heuristic function 2 - checking enemies in line (single direction) with no regards to the stack
    value of the pieces.

    @param state : given current state
    @return      : the heuristic of said state (estimated number of moves to goal)
    """

    board = state.board
    num_moves = 0
    spreaded = {}
    dict_dir = {}

    # checks whether player piece is on the same direction as any direction with enemy piece
    player_pieces = {}

    for pos in board:
        x, y = pos
        tp, val = board[pos]
        if tp == PLAYER:
            if pos not in player_pieces:
                player_pieces[pos] = 0
            continue

        # initialize the piece entry in direction dictionary
        dict_dir[(x, y, (1, 0))] = []
        dict_dir[(x, y, (0, 1))] = []
        dict_dir[(x, y, (1, -1))] = []

        # for every other piece on the board - if player then player on direction
        for _pos in board:
            _x, _y = _pos
            _tp, _val = board[_pos]
            if _tp == PLAYER:
                player_pieces[pos] = 1
                continue

            # x-direction
            if _x == x and _y != y:
                dict_dir[(x, y, (1, 0))].append(_pos)

            # y-direction
            elif _x != x and _y != y:
                dict_dir[(x, y, (0, 1))].append(_pos)

            # vertical direction
            elif _x != x and _y != y:
                x_diff = x - _x
                y_diff = y - _y
                diff = abs(x_diff + y_diff)
                if diff == 0 or diff == SIZE:
                    dict_dir[(x, y, (1, -1))].append(_pos)

        # delete empty enemy entries - implying that they do not share direction with any other pieces
        # empty enemy entries also imply that they require at least 1 additional move to be spread on
        empty = 0
        if not dict_dir[(x, y, (1, 0))]:
            del dict_dir[(x, y, (1, 0))]
            empty += 1
        if not dict_dir[(x, y, (0, 1))]:
            del dict_dir[(x, y, (0, 1))]
            empty += 1
        if not dict_dir[(x, y, (1, -1))]:
            del dict_dir[(x, y, (1, -1))]
            empty += 1
        num_moves += (empty == 3)

    # whether any player piece is on same direction as any "enemy direction"
    num_moves += not any(player_pieces.values())
    del player_pieces

    # then sort the direction dictionary by direction with the highest number of enemy pieces
    dir_sort = list(map(lambda tup: (-len(tup[1]), tup[1]), dict_dir.items()))
    del dict_dir

    # due to it being min-heap (no max heap in Python3), we push negative lengths
    found = False
    heapq.heapify(dir_sort)
    while dir_sort:
        neg_len, pieces = heapq.heappop(dir_sort)
        for piece in pieces:
            found = piece not in spreaded
            spreaded[piece] = 1
        num_moves += found
        del pieces

    return num_moves


def get_neighbors(state: State) -> [tuple]:
    """
    Get all neighboring state of a given, current state of the board. Neighbors are all derived states
    resulted from player's single move.

    @param state : given current state
    @return      : list of all possible single move by player that returns a neighboring state
    """
    neighbors = []
    board = state.board
    for x, y in board.keys():
        p_type, stack = board[(x, y)]
        if p_type == ENEMY:
            continue
        for dir_x, dir_y in all_dir:
            neighbors.append((x, y, dir_x, dir_y))
    return neighbors
