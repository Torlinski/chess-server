#argument parser
#server that takes in commands
#runs move commands on board
import argparse
import logging
import socket
import sys

from src.chess_server.parser import valid_msg, msg_to_move, write_msg
from src.chess_server.engine import Board


parser = argparse.ArgumentParser(description="Chess Server")
parser.add_argument("-v", help="activate the verbose mode", action="store_true")
parser.add_argument("-i", help="IP address of the interface (default 127.0.0.1)",
    default="127.0.0.1")
parser.add_argument("-p", help="port for server listens on (default 2000)",
    type=int, default=2000)
args = parser.parse_args()

HOST = args.i
PORT = args.p
if args.v:
    logging.basicConfig(level=logging.DEBUG)

def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)

def run_local():
    board = Board()
    send_reply(board.display_board())
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
    #run_local()
    run()
