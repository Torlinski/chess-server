Follow instructions in INSTALL.txt to install the dependencies.

Documentation is found in /docs, including how to issue chess moves to the client.

To start the server, run:
python -m src.chess_server [-v] [-i 127.0.0.1] [-p 2000] [-h]

To start the client, run:
python -m src.chess_client [-v] [-i 127.0.0.1] [-p 2000] [-f /test/game/game_01] [-h]

NOTE:
Server/client unfinished. Server can be ran as above, with input being typed in  on the terminal the server is running on with the syntax of the spec.

TODO:
setup client/server communication
checkmate logic (if king can't move, find checker, take/block checker)
file input for client
logging to file
enforce alternate turns with 2 clients
double check chess rules
