# IMPORTS
import queue
from .heuristic import get_heuristic_priority
from .program import check_victory

# GLOBAL VARIALBES
x_dir = [0, -1, -1, 0, 1, 1]
y_dir = [1, 1, 0, -1, -1, 0]
all_dir = [(x_dir[i], y_dir[i]) for i in range(len(x_dir))]


def A_star(state):
    discovered = queue.PriorityQueue()	# pq for discovered nodes, min-heap to check quickly if leaf > other leafs
    parents    = {}		# the immediate parent of a current node
    g_cost     = {}		# real cumulative cost from root
    f_cost     = {}		# best guess f = g + h

    discovered.put(state)		# init state has now been discovered
    g_cost[state] = 0
    # f_cost[root] = h(state, state)
    f_cost[state] = 0

    curr_state = state

    while not discovered.empty():
        curr_state = discovered.get()
        if check_victory(curr_state):
            # make a function that instead of popping the discovered nodes
            # we check for the pq of all leaf nodes
            return reconstruct_path(parents, curr_state)

        for dir in all_dir:			  # for each child node of current
            new_state = curr_state.copy()
            spread(root, dir, new_state)
            g_cost_accum = g_cost(curr_state) + 1 # true cost from init to new_state via curr_state

            if new_state not in g_cost or g_cost_accum < g_cost[new_state]:
                parents[new_state] = curr_state
                g_cost[new_state] = g_cost_accum
                f_cost[new_state] = g_cost_accum + h(new_state)
                if new_state not in discovered:
                    discovered.push(new_state)
                h(new_state)
    return None

# ----------------------------------------------- HELPER FUNCTIONS FOR A STAR SEARCH ----------------------------------------------

def reconstruct_path():
    return