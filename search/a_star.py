# IMPORTS
import queue
from .heuristic import get_heuristic_priority
from .program import check_victory, spread
from .state import State

# GLOBAL VARIALBES
x_dir = [0, -1, -1, 0, 1, 1]
y_dir = [1, 1, 0, -1, -1, 0]
all_dir = [(x_dir[i], y_dir[i]) for i in range(len(x_dir))]
PLAYER = 'r'
ENEMY = 'b'


def A_star(board):
    min_found  = queue.PriorityQueue()	# pq for discovered nodes, min-heap to check quickly if leaf > other leafs
    parents    = {}		# the immediate parent of a current node
    g_cost     = {}		# real cumulative cost from root
    f_cost     = {}		# best guess f = g + h
    discovered = {}

    curr_state = State(board, [])

    min_found.put(curr_state)		# init state has now been discovered
    discovered[curr_state] = 1
    g_cost[curr_state] = 0
    # f_cost[root] = h(state, state)
    f_cost[curr_state] = 0

    while not min_found.empty():
        curr_state = min_found.get()
        del discovered[curr_state]
        if check_victory(curr_state.board):
            # make a function that instead of popping the discovered nodes
            # we check for the pq of all leaf nodes
            return curr_state.moves
        
        for neighbor in get_neighbors(curr_state):
            new_state = State.copy_state(curr_state)
            _ = spread((neighbor[0], neighbor[1]), (neighbor[2], neighbor[3]), new_state.board)
            g_cost_accum = g_cost[curr_state] + 1 # true cost from init to new_state via curr_state

            if new_state not in g_cost or g_cost_accum < g_cost[new_state]:
                parents[new_state] = curr_state
                g_cost[new_state] = g_cost_accum
                f_cost[new_state] = g_cost_accum + h(new_state)
                if new_state not in discovered.keys():
                    discovered[new_state] = 1
                    min_found.put(new_state)
    return None

# ----------------------------------------------- HELPER FUNCTIONS FOR A STAR SEARCH ----------------------------------------------
def h(state: dict[tuple, tuple]):
    return 0

def get_neighbors(state: State) -> list:
    neighbors = []
    board = state.board
    for key in board.keys():
        if board[key][0] == ENEMY:
            continue
        for dir in all_dir:
            neighbors.append((key[0], key[1], dir[0], dir[1]))
    return neighbors
