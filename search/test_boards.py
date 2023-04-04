"""
    Authors : The Duy Nguyen (1100548) and Ramon Javier L. Felipe VI (1233281)
    Module  : test_board.py
    Purpose : Including all user-defined test cases.
"""


all_boards = {
    # Test case from the assignment
    "test_case": {
        (5, 6): ("r", 2),
        (1, 0): ("b", 2),
        (1, 1): ("b", 1),
        (3, 2): ("b", 1),
        (1, 3): ("b", 3)
    },
    "test_case_2": {
        (5, 6): ("r", 2),
        (1, 0): ("b", 2),
        (1, 1): ("b", 1),
        (3, 2): ("b", 1),
        (1, 3): ("b", 3),
        (3, 1): ("r", 1)
    },

    "priority_fail": {
        (4, 2): ("r", 4),
        (4, 3): ("b", 1),
        (2, 2): ("b", 1),
        (1, 2): ("b", 1),
        (0, 2): ("b", 1)
    },

    # Test case where the kill was suboptimal to ending the game earlier
    "suboptimal_kill": {
        (4, 4): ("r", 1),
        (4, 5): ("r", 1),
        (5, 4): ("b", 3),
        (5, 3): ("b", 4),
        (5, 2): ("b", 1),
        (5, 1): ("b", 6)
    },

    # Problem addresses that even if the blue piece with higher problem should be picked, it treats both as equal
    "weight_problem": {
        (4, 1): ("r", 1),
        (4, 5): ("r", 1),
        (5, 4): ("b", 3),
        (5, 3): ("b", 4),
        (5, 2): ("b", 1),
        (5, 1): ("b", 6)
    },

    # Use these boards to test distance heuristic if it actually underestimates
    "complex_1": {
        (1, 2): ("r", 3),
        (1, 3): ("b", 1),
        (0, 5): ("b", 1),
        (3, 1): ("b", 3),
        (3, 2): ("b", 1),
        (5, 1): ("b", 2),
        (5, 2): ("b", 1),
        (5, 3): ("b", 1),
        (4, 4): ("b", 2),
        (3, 4): ("b", 2),
        (2, 5): ("b", 1),
        (3, 6): ("b", 1),
        (5, 5): ("b", 1)
    },
    "complex_2": {
        (1, 0): ("r", 3),
        (2, 3): ("r", 1),
        (3, 4): ("b", 2),
        (2, 5): ("b", 1),
        (3, 1): ("b", 3),
        (3, 2): ("b", 1),
        (5, 1): ("b", 2),
        (3, 6): ("b", 1),
        (5, 5): ("b", 1),
        (1, 3): ("b", 1),
        (0, 5): ("b", 1),
        (5, 2): ("b", 1),
        (1, 2): ("r", 3),
        (5, 3): ("b", 1),
        (4, 4): ("b", 2)
    },
    "complex_3": {
        (1, 1): ("r", 2),
        (1, 2): ("r", 6),
        (1, 5): ("b", 2),
        (3, 5): ("b", 1),
        (4, 5): ("b", 1),
        (4, 4): ("b", 1),
        (5, 4): ("b", 1),
        (4, 3): ("b", 3),
        (5, 2): ("b", 1),
        (4, 1): ("b", 1)
    },

    # sparse test cases
    "sparse_1": {
        (1, 1): ("r", 2),
        (2, 3): ("r", 1),
        (5, 2): ("r", 1),
        (4, 5): ("r", 3),
        (4, 1): ("b", 3),
        (3, 4): ("b", 2),
    },
    "sparse_2": {
        (1, 1): ("r", 2),
        (2, 3): ("r", 1),
        (5, 2): ("r", 1),
        (0, 6): ("r", 2),
        (4, 1): ("b", 3),
        (3, 4): ("b", 2),
        (4, 6): ("b", 1)
    },
    # sparse with stacked red
    "sparse_ps": {
        (1, 1): ("b", 2),
        (2, 3): ("r", 4),
        (5, 2): ("r", 3),
        (0, 6): ("b", 2),
        (4, 1): ("b", 3),
        (3, 4): ("b", 2),
        (4, 6): ("b", 1)
    },
    # sparse with stacked blue
    "sparse_es": {
        (1, 1): ("r", 1),
        (2, 3): ("b", 4),
        (5, 2): ("b", 3),
        (0, 6): ("r", 1),
        (4, 4): ("r", 1),
        (4, 6): ("r", 1)
    },

    # Extremely dense, all-1
    "all_1_48": {
        (0, 0): ("b", 1),
        (0, 1): ("b", 1),
        (0, 2): ("b", 1),
        (0, 3): ("b", 1),
        (0, 4): ("b", 1),
        (0, 5): ("b", 1),
        (0, 6): ("b", 1),

        (1, 0): ("b", 1),
        (1, 1): ("r", 1),
        (1, 2): ("b", 1),
        (1, 3): ("b", 1),
        (1, 4): ("b", 1),
        (1, 5): ("b", 1),
        (1, 6): ("b", 1),

        (2, 0): ("b", 1),
        (2, 1): ("b", 1),
        (2, 2): ("b", 1),
        (2, 3): ("b", 1),
        (2, 4): ("b", 1),
        (2, 5): ("b", 1),
        (2, 6): ("b", 1),

        (3, 0): ("b", 1),
        (3, 1): ("b", 1),
        (3, 2): ("b", 1),
        (3, 3): ("b", 1),
        (3, 4): ("b", 1),
        (3, 5): ("b", 1),
        (3, 6): ("b", 1),

        (4, 0): ("b", 1),
        (4, 1): ("b", 1),
        (4, 2): ("b", 1),
        (4, 3): ("b", 1),
        (4, 4): ("b", 1),
        (4, 5): ("b", 1),
        (4, 6): ("b", 1),

        (5, 0): ("b", 1),
        (5, 1): ("b", 1),
        (5, 2): ("b", 1),
        (5, 3): ("b", 1),
        (5, 4): ("b", 1),
        (5, 5): ("b", 1),
        (5, 6): ("b", 1),

        (6, 0): ("b", 1),
        (6, 1): ("b", 1),
        (6, 2): ("b", 1),
        (6, 3): ("b", 1),
        (6, 4): ("b", 1),
        (6, 5): ("b", 1),
        (6, 6): ("b", 1),
    },
    "all_12_37": {
        (0, 0): ("r", 1),
        (0, 1): ("b", 1),
        (0, 2): ("b", 1),
        (0, 3): ("r", 1),
        (0, 4): ("b", 1),
        (0, 5): ("b", 1),
        (0, 6): ("b", 1),

        (1, 0): ("b", 1),
        (1, 1): ("r", 1),
        (1, 2): ("b", 1),
        (1, 3): ("b", 1),
        (1, 4): ("b", 1),
        (1, 5): ("b", 1),
        (1, 6): ("b", 1),

        (2, 0): ("b", 1),
        (2, 1): ("r", 1),
        (2, 2): ("b", 1),
        (2, 3): ("b", 1),
        (2, 4): ("b", 1),
        (2, 5): ("r", 1),
        (2, 6): ("b", 1),

        (3, 0): ("r", 1),
        (3, 1): ("b", 1),
        (3, 2): ("b", 1),
        (3, 3): ("b", 1),
        (3, 4): ("r", 1),
        (3, 5): ("b", 1),
        (3, 6): ("b", 1),

        (4, 0): ("r", 1),
        (4, 1): ("b", 1),
        (4, 2): ("b", 1),
        (4, 3): ("b", 1),
        (4, 4): ("r", 1),
        (4, 5): ("b", 1),
        (4, 6): ("b", 1),

        (5, 0): ("b", 1),
        (5, 1): ("b", 1),
        (5, 2): ("r", 1),
        (5, 3): ("b", 1),
        (5, 4): ("b", 1),
        (5, 5): ("b", 1),
        (5, 6): ("r", 1),

        (6, 0): ("b", 1),
        (6, 1): ("b", 1),
        (6, 2): ("b", 1),
        (6, 3): ("b", 1),
        (6, 4): ("r", 1),
        (6, 5): ("b", 1),
        (6, 6): ("b", 1),
    },
    "all_23_26": {
        (0, 0): ("r", 1),
        (0, 1): ("b", 1),
        (0, 2): ("r", 1),
        (0, 3): ("r", 1),
        (0, 4): ("b", 1),
        (0, 5): ("b", 1),
        (0, 6): ("b", 1),

        (1, 0): ("b", 1),
        (1, 1): ("r", 1),
        (1, 2): ("b", 1),
        (1, 3): ("b", 1),
        (1, 4): ("r", 1),
        (1, 5): ("b", 1),
        (1, 6): ("r", 1),

        (2, 0): ("b", 1),
        (2, 1): ("r", 1),
        (2, 2): ("b", 1),
        (2, 3): ("r", 1),
        (2, 4): ("b", 1),
        (2, 5): ("r", 1),
        (2, 6): ("b", 1),

        (3, 0): ("r", 1),
        (3, 1): ("b", 1),
        (3, 2): ("r", 1),
        (3, 3): ("b", 1),
        (3, 4): ("r", 1),
        (3, 5): ("r", 1),
        (3, 6): ("b", 1),

        (4, 0): ("r", 1),
        (4, 1): ("b", 1),
        (4, 2): ("b", 1),
        (4, 3): ("r", 1),
        (4, 4): ("r", 1),
        (4, 5): ("b", 1),
        (4, 6): ("r", 1),

        (5, 0): ("r", 1),
        (5, 1): ("b", 1),
        (5, 2): ("r", 1),
        (5, 3): ("r", 1),
        (5, 4): ("b", 1),
        (5, 5): ("r", 1),
        (5, 6): ("r", 1),

        (6, 0): ("b", 1),
        (6, 1): ("b", 1),
        (6, 2): ("b", 1),
        (6, 3): ("b", 1),
        (6, 4): ("r", 1),
        (6, 5): ("b", 1),
        (6, 6): ("b", 1),
    },
    "all_37_12": {
        (0, 0): ("r", 1),
        (0, 1): ("r", 1),
        (0, 2): ("b", 1),
        (0, 3): ("r", 1),
        (0, 4): ("r", 1),
        (0, 5): ("b", 1),
        (0, 6): ("r", 1),

        (1, 0): ("r", 1),
        (1, 1): ("r", 1),
        (1, 2): ("b", 1),
        (1, 3): ("r", 1),
        (1, 4): ("b", 1),
        (1, 5): ("r", 1),
        (1, 6): ("r", 1),

        (2, 0): ("r", 1),
        (2, 1): ("r", 1),
        (2, 2): ("b", 1),
        (2, 3): ("r", 1),
        (2, 4): ("b", 1),
        (2, 5): ("r", 1),
        (2, 6): ("b", 1),

        (3, 0): ("r", 1),
        (3, 1): ("b", 1),
        (3, 2): ("b", 1),
        (3, 3): ("b", 1),
        (3, 4): ("r", 1),
        (3, 5): ("b", 1),
        (3, 6): ("r", 1),

        (4, 0): ("r", 1),
        (4, 1): ("b", 1),
        (4, 2): ("b", 1),
        (4, 3): ("r", 1),
        (4, 4): ("r", 1),
        (4, 5): ("b", 1),
        (4, 6): ("r", 1),

        (5, 0): ("b", 1),
        (5, 1): ("r", 1),
        (5, 2): ("r", 1),
        (5, 3): ("b", 1),
        (5, 4): ("b", 1),
        (5, 5): ("r", 1),
        (5, 6): ("r", 1),

        (6, 0): ("b", 1),
        (6, 1): ("b", 1),
        (6, 2): ("b", 1),
        (6, 3): ("b", 1),
        (6, 4): ("r", 1),
        (6, 5): ("b", 1),
        (6, 6): ("b", 1),
    },
    "all_43_5": {
        (0, 0): ("r", 1),
        (0, 1): ("r", 1),
        (0, 2): ("b", 1),
        (0, 3): ("r", 1),
        (0, 4): ("r", 1),
        (0, 5): ("r", 1),
        (0, 6): ("r", 1),

        (1, 0): ("r", 1),
        (1, 1): ("b", 1),
        (1, 2): ("r", 1),
        (1, 3): ("b", 1),
        (1, 4): ("r", 1),
        (1, 5): ("r", 1),
        (1, 6): ("r", 1),

        (2, 0): ("r", 2),
        (2, 1): ("r", 1),
        (2, 2): ("r", 1),
        (2, 3): ("r", 1),
        (2, 4): ("r", 1),
        (2, 5): ("r", 1),
        (2, 6): ("r", 1),

        (3, 0): ("r", 1),
        (3, 1): ("r", 1),
        (3, 2): ("r", 1),
        (3, 3): ("r", 1),
        (3, 4): ("b", 1),
        (3, 5): ("r", 1),
        (3, 6): ("r", 1),

        (4, 0): ("r", 1),
        (4, 1): ("r", 1),
        (4, 2): ("r", 1),
        (4, 3): ("r", 1),
        # (4, 4): ("r", 1),
        (4, 5): ("r", 1),
        (4, 6): ("r", 1),

        (5, 0): ("r", 1),
        (5, 1): ("r", 1),
        (5, 2): ("r", 1),
        (5, 3): ("r", 1),
        (5, 4): ("b", 1),
        (5, 5): ("r", 1),
        (5, 6): ("r", 1),

        (6, 0): ("r", 1),
        (6, 1): ("r", 1),
        (6, 2): ("r", 1),
        (6, 3): ("r", 1),
        (6, 4): ("r", 1),
        (6, 5): ("r", 1),
        (6, 6): ("r", 1),
    },
    "all_31_18": {
        (0, 0): ("r", 1),
        (0, 1): ("r", 1),
        (0, 2): ("b", 1),
        (0, 3): ("b", 1),
        (0, 4): ("r", 1),
        (0, 5): ("r", 1),
        (0, 6): ("b", 1),

        (1, 0): ("r", 1),
        (1, 1): ("b", 1),
        (1, 2): ("r", 1),
        (1, 3): ("r", 1),
        (1, 4): ("b", 1),
        (1, 5): ("r", 1),
        (1, 6): ("r", 1),

        (2, 0): ("r", 1),
        (2, 1): ("b", 1),
        (2, 2): ("r", 1),
        (2, 3): ("r", 1),
        (2, 4): ("b", 1),
        (2, 5): ("r", 1),
        (2, 6): ("r", 1),

        (3, 0): ("r", 1),
        (3, 1): ("b", 1),
        (3, 2): ("b", 1),
        (3, 3): ("r", 1),
        (3, 4): ("b", 1),
        (3, 5): ("r", 1),
        (3, 6): ("b", 1),

        (4, 0): ("r", 1),
        (4, 1): ("r", 1),
        (4, 2): ("b", 1),
        (4, 3): ("r", 1),
        (4, 4): ("b", 1),
        (4, 5): ("r", 1),
        (4, 6): ("r", 1),

        (5, 0): ("b", 1),
        (5, 1): ("r", 1),
        (5, 2): ("r", 1),
        (5, 3): ("r", 1),
        (5, 4): ("b", 1),
        (5, 5): ("r", 1),
        (5, 6): ("b", 1),

        (6, 0): ("r", 1),
        (6, 1): ("r", 1),
        (6, 2): ("r", 1),
        (6, 3): ("r", 1),
        (6, 4): ("r", 1),
        (6, 5): ("b", 1),
        (6, 6): ("b", 1),
    },

    # Dense, all-2 (best, and almost worst)
    "all_2_1": {
        (1, 1): ("r", 2),
        (1, 2): ("b", 2),
        (1, 5): ("b", 2),
        (3, 5): ("b", 2),
        (4, 5): ("b", 2),
        (1, 6): ("b", 2),
        (5, 4): ("b", 2),
        (4, 3): ("b", 2),

        (5, 1): ("b", 2),
        (6, 2): ("b", 2),
        (5, 3): ("b", 2),
        (5, 5): ("b", 2),
        (6, 5): ("b", 2),
        (6, 6): ("b", 2),
        (6, 3): ("b", 2),
        (4, 2): ("b", 2),
        (3, 3): ("b", 2),
        (3, 1): ("b", 2),

        (4, 1): ("b", 2),
        (0, 0): ("b", 2),
        (1, 0): ("b", 2),
        (2, 0): ("b", 2),
        (6, 0): ("b", 2),
        (0, 1): ("b", 2)
    },
    "all_2_2": {
        (1, 1): ("r", 2),
        (1, 2): ("b", 2),
        (1, 5): ("b", 2),
        (3, 5): ("b", 2),
        (4, 5): ("b", 2),
        (1, 6): ("b", 2),
        (5, 4): ("b", 2),
        (4, 3): ("b", 2),

        (5, 1): ("b", 2),
        (6, 2): ("b", 2),
        (5, 3): ("b", 2),
        (5, 5): ("b", 2),
        (6, 5): ("b", 2),
        (6, 6): ("b", 2),
        (6, 3): ("b", 2),
        (4, 2): ("b", 2),
        (3, 3): ("b", 2),
        (3, 1): ("b", 2),

        (4, 1): ("b", 2),
        (0, 0): ("b", 2),
        (1, 0): ("b", 2),
        (2, 0): ("b", 2),
        (0, 4): ("b", 2),
        (0, 1): ("b", 2)
    }
}
