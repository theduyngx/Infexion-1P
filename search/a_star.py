# IMPORTS
import queue
# from heuristic import get_heuristic_priority
from program import check_victory, spread, INF
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
    hash_curr  = curr_state.to_hash()
    min_found.put(curr_state)		    # init state has now been discovered
    discovered[hash_curr] = 1
    g_cost[hash_curr]     = 0
    f_cost[hash_curr]     = 0
    # min_moves = []
    # num_moves = INF

    while not min_found.empty():
        curr_state = min_found.get()
        hash_curr  = curr_state.to_hash()
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
            hash_new = new_state.to_hash()
            # true cost from init to new_state via curr_state
            g_cost_accum = g_cost[hash_curr] + 1

            if hash_new not in g_cost or g_cost_accum < g_cost[hash_new]:
                g_cost[hash_new] = g_cost_accum
                f_cost[hash_new] = g_cost_accum + h(new_state)
                new_state.f_cost  = f_cost[hash_new]
                if new_state not in discovered:
                    discovered[hash_new] = 1
                    min_found.put(new_state)
    return []


def h(state: State) -> int:
    """
    Heuristic function.
    """
    return not check_victory(state.board)


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
