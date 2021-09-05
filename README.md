# Chess Server

## Description

The Chess Server is an personal project that aims to create a chess server that can
parse, validate and execute chess moves when instructions are sent to it by connected
clients and hence allow two players to play chess together.


## Installation

To run the code in this repository on your local computer, you will need to clone this
github repository onto your computer, and then install the library from the path that
it has been cloned to.

### Cloning the repo

Open a terminal window, navigate to the desired directory and run:
```
git clone https://github.com/Torlinski/chess-server.git
```
This will create a new `chess-server` directory which you should navigate to using:
```
cd chess-server
```

### Installing dependencies
This repo doesn't currently have any external library dependencies for running.
However, it does use pytest for testing. You may wish to create and activate a virtual
environment for working on this project. For more information on virtual environments,
visit [this page](https://realpython.com/python-virtual-environments-a-primer/). Then run:
``` 
pip install -e . 
```
This will install the library as well as its dependencies into your environment, enabling
you to run all the code in this repository locally.

## Usage

### Setup
To start the server, run:
```bash
python -m chess_server [-v] [-i 127.0.0.1] [-p 2000] [-h]
```

`-v`: Activate verbose mode
`-i`: IP Address of the interface to bind (default 127.0.0.1)
`-p`: Port for listening for new connections (default 2000)
`-h`: Display help

To start the client, run:
```bash
python -m chess_client [-v] [-i 127.0.0.1] [-p 2000] [-f /test/game/game_01] [-h]
```

`-v`: Activate verbose mode
`-i`: IP Address of the chess server (default 127.0.0.1)
`-p`: Port of the chess server (default 2000)
`-f`: File input of a game
`-h`: Display help

### Gameplay

Once clients are connected the first player may begin by entering their move (by default
the first client to connect to and always the controller of the white pieces). The server
uses [standard chess rules](https://en.wikipedia.org/wiki/Rules_of_chess).

Simple [from]-[to] notation is used to denote chess moves. For example to move a pawn
from e2 to e4 the player would enter `e2-e4`. If the entered move is invalid the player
will be notified and will have to enter a valid move. The players alternate entering
valid moves until checkmate is achieved or insufficient pieces are left to do so (not yet
implemented).

## Testing

To run tests run `python -m pytest` while in the root directory of the repo.

This should gather and execute all tests in the test dir with pytest.

## TODO
* setup non-local client/server communication
* checkmate logic (if king can't move, find checker, take/block checker)
* file input for client
* logging to file
* enforce alternate turns with 2 clients
* double check chess rules (en passant?)
