all_boards = {
    # Test case from the assignment
    "test_case": {
        (5, 6): ("r", 2),
        (1, 0): ("b", 2),
        (1, 1): ("b", 1),
        (3, 2): ("b", 1),
        (1, 3): ("b", 3)
    },

    # Test case where the kill was suboptimal
    # to ending the game earier
    "suboptimal_kill" : {
        # (2,2): ("r", 3),
        # (2,1): ("b", 1),
        # (2,0): ("b", 1),
        # (3,6): ("r", 1),
        (4,4): ("r", 1),
        (4,5): ("r", 1),
        (5,4): ("b", 3),
        (5,3): ("b", 4),
        (5,2): ("b", 1),
        (5,1): ("b", 6)
    },

    # Problem addresses that even if the blue piece
    # with higher problem should be picked, it treats both as equal
    "weight_problem" : {
        (4,1): ("r", 1),
        (4,5): ("r", 1),
        (5,4): ("b", 3),
        (5,3): ("b", 4),
        (5,2): ("b", 1),
        (5,1): ("b", 6)
    },

    # Use these boards to test distance heuristic if it actually underestimate
    "distance_test_1": {
        (4,4): ("r", 1),
        (4,5): ("r", 1)
    }
}