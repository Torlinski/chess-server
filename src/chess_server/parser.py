#Turns server commands into move instructions
#and move history into response messages
import re

def valid_msg(msg):
    if msg == "display_board":
        return True
    pattern = r'^([a-h][1-8])-([a-h][1-8])$'
    if re.search(pattern, msg):
        return True
    return False

def msg_to_move(msg):
    pattern = r'^([a-h][1-8])-([a-h][1-8])$'
    squares = re.search(pattern, msg)
    if squares:
        return (square_to_tuple(squares[1]),
                square_to_tuple(squares[2]))

def write_msg(move):
    """
    Returns message string based on move from move_history
    """
    X = move[0]
    case_src = tuple_to_square(move[1])
    piece = symbol_to_name(move[2])
    case_dest = tuple_to_square(move[3])
    target = symbol_to_name(move[4]) if move[4] else ""
    check = ". Check" if move[5] else ""

    if castling_check(piece, case_src, case_dest):
        msg = f"{X}. {piece} does a {castling_type} "\
              f"castling from {case_src} to {case_dest}{check}"
    elif target:
        msg = f"{X}. {piece} on {case_src} takes {target} "\
              f"on {case_dest}{check}"
    else:
        msg = f"{X}. {piece} moves from {case_src} to {case_dest}{check}"
    return msg

def symbol_to_name(symbol):
    symbol_map = {
        "p": "pawn",
        "r": "rook",
        "c": "knight",
        "b": "bishop",
        "q": "queen",
        "k": "king"
        }
    if symbol.isupper():
        piece_name = "white "
    else:
        piece_name = "black "
    piece_name += symbol_map[symbol.lower()]
    return piece_name

def square_to_tuple(square):
    letter_to_number = {"a": 1, "b": 2, "c": 3, "d": 4,
                        "e": 5, "f": 6, "g": 7, "h": 8}
    return (letter_to_number[square[0]], int(square[1]))

def tuple_to_square(pos):
    number_to_letter = {1: "a", 2: "b", 3: "c", 4: "d",
                        5: "e", 6: "f", 7: "g", 8: "h"}
    return number_to_letter[pos[0]] + str(pos[1])

def castling_check(piece, from_pos, to_pos):
    if piece in ("k", "K"):
        if from_pos[0] - to_pos[0] in (2, -2):
            return True
    return False
