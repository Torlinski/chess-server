#Turns server commands into move instructions
#and move history into response messages
import re

def validate_msg(msg):
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

def square_to_tuple(square):
    letter_to_number = {"a": 1, "b": 2, "c": 3, "d": 4,
                        "e": 5, "f": 6, "g": 7, "h": 8}
    return (letter_to_number[square[0]], int(square[1]))

def tuple_to_square(pos):
    number_to_letter = {1: "a", 2: "b", 3: "c", 4: "d",
                        5: "e", 6: "f", 7: "g", 8: "h"}
    return pos[0] + str(pos[1])
