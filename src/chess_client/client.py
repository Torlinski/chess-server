import argparse
import os
import socket

parser = argparse.ArgumentParser(description="Chess Client")
parser.add_argument("-v", help="activate the verbose mode", action="store_true")
parser.add_argument("-i", help="IP address of the interface (default 127.0.0.1)",
    default="127.0.0.1")
parser.add_argument("-p", help="port for server listens on (default 2000)",
    type=int, default=2000)
parser.add_argument("-f", help="input file of a game")
args = parser.parse_args()

HOST = args.i
PORT = args.p
if args.v:
    logging.basicConfig(level=logging.DEBUG)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received', repr(data))