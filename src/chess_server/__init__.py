import argparse

import src.chess_server.server as Server

parser = argparse.ArgumentParser(description="Chess Server") 
parser.add_argument("-v", help="activate the verbose mode", action="store_true")
parser.add_argument("-i", help="IP address of the interface (default 127.0.0.1)", 
    default="127.0.0.1") 
parser.add_argument("-p", help="port for server listens on (default 2000)", 
    type=int, default=2000) 
args = parser.parse_args()

Server.run_local()
