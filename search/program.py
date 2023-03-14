# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from utils import render_board

# # constants
# SIZE = 7
# MAX_PTS = SIZE ** 2
#
#
# # get all possible roots
# def get_all_roots(state: dict[tuple, tuple]) -> list[tuple]:
#     total_score = sum(i for i, j in state.values())
#     all_roots = []
#     if total_score < MAX_PTS:
#         for x in range(0, 6):
#             for y in range(0, 6):
#                 if (x, y) in state:
#                     if state[(x, y)][0] == 'b':
#                         continue
#                 all_roots.append((x, y))
#     else:
#         for x, y in state.keys():
#             if state[(x, y)][0] == 'r':
#                 all_roots.append((x, y))
#     return all_roots


def search(state: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """

    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    print(render_board(state, ansi=False))

    # # CODE
    # # get all moves
    # all_roots = get_all_roots(state)
    # min_score = 0
    # for _ in all_roots:
    #     # Do IDS to get the min score of each possible root
    #     # get the min score and from that get ret (the best play to win)
    #     min_score += 1

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    return [
        (5, 6, -1, 1),
        (3, 1, 0, 1),
        (3, 2, -1, 1),
        (1, 4, 0, -1),
        (1, 3, 0, -1)
    ]
