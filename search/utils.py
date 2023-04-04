"""
    Authors : The Duy Nguyen (1100548) and Ramon Javier L. Felipe VI (1233281)
    Module  : utils.py
    Purpose : apply_ansi and render_board are written in The University of Melbourne skeleton code - Project Part A:
              Single Player Infexion, COMP30024 Artificial Intelligence, Semester 1 2023. Utility functions.
"""

from movement import spread


def apply_ansi(string, bold=True, color=None) -> str:
    """
    Wraps a string with ANSI control codes to enable basic terminal-based formatting on that string.

    @param string : string to apply ANSI control codes to
    @param bold   : true if you want the text to be rendered bold
    @param color  : colour of the text.
    @return       : applied ANSI string
    """
    bold_code = "\033[1m" if bold else ""
    color_code = ""
    if color == "r":
        color_code = "\033[31m"
    if color == "b":
        color_code = "\033[34m"
    return f"{bold_code}{color_code}{string}\033[0m"


def render_board(board: dict[tuple, tuple], ansi=True) -> str:
    """
    Visualise the Infexion hex board via a multiline ASCII string. The layout corresponds to the
    axial coordinate system as described in the game specification document.
    
    Example:

        >>> state = {
        ...     (5, 6): ("r", 2),
        ...     (1, 0): ("b", 2),
        ...     (1, 1): ("b", 1),
        ...     (3, 2): ("b", 1),
        ...     (1, 3): ("b", 3),
        ... }
        >>> render_board(state, ansi=True)

                                ..     
                            ..      ..     
                        ..      ..      ..     
                    ..      ..      ..      ..     
                ..      ..      ..      ..      ..     
            b2      ..      b1      ..      ..      ..     
        ..      b1      ..      ..      ..      ..      ..     
            ..      ..      ..      ..      ..      r2     
                ..      b3      ..      ..      ..     
                    ..      ..      ..      ..     
                        ..      ..      ..     
                            ..      ..     
                                ..     
    """
    dim = 7
    output = ""
    for row in range(dim * 2 - 1):
        output += "    " * abs((dim - 1) - row)
        for col in range(dim - abs(row - (dim - 1))):
            # Map row, col to r, q
            r = max((dim - 1) - row, 0) + col
            q = max(row - (dim - 1), 0) + col
            if (r, q) in board:
                color, power = board[(r, q)]
                text = f"{color}{power}".center(4)
                if ansi:
                    output += apply_ansi(text, color=color, bold=False)
                else:
                    output += text
            else:
                output += " .. "
            output += "    "
        output += "\n"
    return output


def get_algorithm_name(f_name: str) -> str:
    """
    Function to get the search algorithm name, just for display.

    @param f_name  : function name
    @return        : algorithm name
    """
    display_name = f_name.replace("_", " ").replace(" star", "*")
    return display_name


def print_sequence_board(board: dict[tuple, tuple], sequence: list[tuple], num_operations: int,
                         algo: str, time_taken: float):
    """
    Print the different boards resulted from a sequence of moves.

    @param board          : the given board
    @param sequence       : sequence of moves
    @param num_operations : required number of generations to generate sequence
    @param algo           : search algorithm name
    @param time_taken     : time taken to execute the search
    """

    print("")
    print("------------------------------------------------------")
    print("------------------- INITIAL STATE --------------------")
    print("------------------------------------------------------")
    print("")
    print(render_board(board))
    print("")
    print("------------------------------------------------------")
    print("----------------------- MOVES ------------------------")
    print("------------------------------------------------------")
    num_move = 0

    for x, y, dx, dy in sequence:
        num_move += 1
        spread((x, y), (dx, dy), board)
        print(f"Move #{num_move}: SPREAD ({x}, {y}) at direction ({dx}, {dy})\n")
        print(render_board(board))
        print("------------------------------------------------------")

    print("-------------------- STATISTICS ----------------------")
    print("------------------------------------------------------")
    print(f"SEARCH ALGORITHM\t\t :\t{algo}")
    print(f"NUMBER OF MOVES\t\t\t :\t{len(sequence)}")
    print(f"NUMBER OF GENERATIONS\t :\t{num_operations}")
    print(f'TOTAL TIME TAKEN\t\t :\t{time_taken}')
