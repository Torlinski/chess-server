#argument parser
#server that takes in commands
#runs move commands on board
from parser import valid_msg, msg_to_move, write_msg
from engine import Board

def run():
    board = Board()
    while True:
        msg = get_msg()
        if not valid_msg(msg):
            send_reply("Invalid request")
        elif msg == "display_board":
            send_reply(board.display_board())
        else:
            move = msg_to_move(msg)
            reply = move_piece(board, move)
            send_reply(reply)

def get_msg():
    return input()

def send_reply(msg):
    print(msg)

def move_piece(board, move):
    success = board.move_piece(*move)
    if success:
        return write_msg(board.move_history[-1])
    else:
        return "Invalid Move"

if __name__ == "__main__":
    run()
