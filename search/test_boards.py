all_boards = {
    # Test case from the assignment
    "test_case": {
        (5, 6): ("r", 2),
        (1, 0): ("b", 2),
        (1, 1): ("b", 1),
        (3, 2): ("b", 1),
        (1, 3): ("b", 3)
    },

    # Test case where the kill was suboptimal to ending the game earlier
    "suboptimal_kill": {
        # (2, 2): ("r", 3),
        # (2, 1): ("b", 1),
        # (2, 0): ("b", 1),
        # (3, 6): ("r", 1),
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
    }
}
