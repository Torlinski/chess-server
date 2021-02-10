import logging
from copy import deepcopy

WHITE="white"
BLACK="black"
CARDINALS = ((1, 0), (0, -1), (-1, 0), (0, 1))
DIAGONALS = ((1, 1), (1, -1), (-1, -1), (-1, 1))
PIECES = ["P", "R", "C", "B", "Q", "K"]
logging.basicConfig(level=logging.DEBUG)

class Board:
    def __init__(self):
        logging.debug("Board initialising")
        self.reset_board()
        self.last_moved_color = BLACK
        self.move_history = []

    def reset_board(self):
        """
        Resets the board (Board.board) to the starting configuration.
        See reference board below.
            a   b   c   d   e   f   g   h
          --------------------------------
        8 | r | c | b | q | k | b | c | r
          --------------------------------
        7 | p | p | p | p | p | p | p | p
          --------------------------------
        6 |   |   |   |   |   |   |   |  
          --------------------------------
        5 |   |   |   |   |   |   |   |  
          --------------------------------
        4 |   |   |   |   |   |   |   |  
          --------------------------------
        3 |   |   |   |   |   |   |   |  
          --------------------------------
        2 | P | P | P | P | P | P | P | P
          --------------------------------
        1 | R | C | B | Q | K | B | C | R
          --------------------------------
            a   b   c   d   e   f   g   h

        board coordinates use (x[1-8], y[1-8]) from bottom left,
        eg. K is in pos (5, 1)
        """
        self.board = {}
        piece_row_order = [
            Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook
            ]
        for x, piece in zip(range(1,9), piece_row_order):
            self.board[(x, 1)] = piece(self.board, WHITE, (x, 1))
            self.board[(x, 2)] = Pawn(self.board, WHITE, (x, 2))
            self.board[(x, 7)] = Pawn(self.board, BLACK, (x, 7))
            self.board[(x, 8)] = piece(self.board, BLACK, (x, 8))

    def move_piece(self, from_pos, to_pos):
        """
        Moves piece if move is valid with piece + check rules
        Does this by copying the board, and checking if carrying out the move
        results in a valid configuration, replacing the board with the copy
        and adding to self.move_history if true, and reverting if not.

        Arguments:
            from_pos: tuple in form (x, y) where x is current column of the 
                piece and y is the current row of the piece, both int 1-8
            to_pos: tuple in form (x, y) where x is desired column of the
                piece and y is the desired row of the piece, both int 1-8

        Returns:
            True/False if piece was moved successfully

        """
        if not self.board.get(from_pos):
            logging.debug("No piece in selected position")
            return False
        if self.board[from_pos].color == self.last_moved_color:
            logging.debug("Attempting to move wrong color")
            return False
        if self.board[from_pos].verify_move(to_pos):
            logging.debug(f"Move from {from_pos} to {to_pos} in piece valid moves")
            #going to try move and revert if puts king in check
            Board_copy = deepcopy(self)
            if self._move_not_castling(from_pos, to_pos):
                Board_copy._force_move_piece(from_pos, to_pos)
            else:
                Board_copy._force_castling(from_pos, to_pos)
            Board_copy.last_moved_color = Board_copy.board[to_pos].color
            if not Board_copy.king_in_check(Board_copy.last_moved_color):
                logging.debug(f"Move does not place own king in check")
                check_enemy = Board_copy.king_in_check(self.last_moved_color)
                self.add_to_history(from_pos, to_pos, check_enemy)
                self.board = Board_copy.board
                self.last_moved_color = Board_copy.last_moved_color
                return True
            logging.debug(f"Move places own king in check")
            return False

    def _force_move_piece(self, from_pos, to_pos):
        """
        Moves a piece regardless of the moves validity
        """
        self.board[to_pos] = self.board[from_pos]
        self.board[from_pos].pos = to_pos
        if self.board[to_pos].symbol in ('K', 'k', 'R', 'r'):
            self.board[to_pos].has_moved = True
        del self.board[from_pos]

    def _move_not_castling(self, from_pos, to_pos):
        """
        Returns true if move not castling
        """
        castling_moves = [
            ((5, 1), (7, 1)),
            ((5, 1), (3, 1)),
            ((5, 8), (7, 8)),
            ((5, 8), (3, 8))
        ]
        if self.board[from_pos].symbol in ('K', 'k'):
            if (from_pos, to_pos) in castling_moves:
                return False
        return True

    def _force_castling(self, from_pos, to_pos):
        """
        Completes castling regardless of move validity
        """
        from_rook_pos = (8 if to_pos[0] == 7 else 1, to_pos[1])
        to_rook_pos = (6 if to_pos[0] == 7 else 4, to_pos[1])
        self._force_move_piece(from_pos, to_pos) #moves king
        self._force_move_piece(from_rook_pos, to_rook_pos)

    def add_to_history(self, from_pos, to_pos, check_enemy_king):
        """
        Adds to move_history, appends:
            original position tuple,
            select piece symbol,
            target position tuple,
            target position occupant (if any),
            Bool whether enemy king is put in check
        """
        self.move_history.append([
            from_pos,
            self.board[from_pos].symbol,
            to_pos,
            self.board[to_pos].symbol if self.board.get(to_pos) else None,
            check_enemy_king
        ])

    def king_in_check(self, color):
        """
        Returns True if a king of a certain color is in check
        """
        if color == WHITE:
            king_pos = self.find_piece("K")
        if color == BLACK:
            king_pos = self.find_piece("k")
        return self._position_in_check(king_pos, color)

    def find_piece(self, symbol):
        """
        Returns position tuple of first piece with said symbol
        """
        for piece in self.board.values():
            if piece.symbol == symbol:
                return piece.pos

    def _position_in_check(self, pos, color):
        """
        Return True if a position would be in check for a king of a certain color
        """
        for piece in self.board.values():
            if color == WHITE:
                if piece.color == BLACK:
                    if piece.verify_move(pos):
                        return True
            if color == BLACK:
                if piece.color == WHITE:
                    if piece.verify_move(pos):
                        return True
        return False

    def display_board(self):
        """
        Creates a pretty board for display_board server command

        Returns:
            string of pretty board (19 lines)
        """
        board_symbol_list = self._create_board_symbol_list()
        col_str = "    a   b   c   d   e   f   g   h\n"
        row_divider = "  --------------------------------\n"
        row_template = "{} | {} | {} | {} | {} | {} | {} | {} | {}\n"
        pretty_board = col_str + row_divider
        for row in board_symbol_list:
            pretty_board += row_template.format(*row)
            pretty_board += row_divider
        pretty_board += col_str
        logging.debug("\n" + pretty_board)
        return pretty_board
        

    def _create_board_symbol_list(self):
        """
        Creates list of lists, with each item being a space, to represent
        no piece, or the piece's symbol.

        Returns:
            list (8x9), inside 8 lists consisting of rows, descending
              inside each sublist there is the row num and 8 symbols, ascending
              eg. rows[0][1] = occupant of a8, if any

        """
        rows = []
        for y in range(8,0,-1):
            row = [y]
            for x in range(1,9):
                if self.board.get((x, y)):
                    row.append(self.board[(x,y)].symbol)
                else:
                    row.append(" ")
            rows.append(row)
        return rows

class Piece:
    def __init__(self, board, color, pos):
        self.board = board
        self.color = color
        self.pos = pos

    def verify_move(self, to_pos):
        """
        Returns True if move in list of moves. List of moves specific to type of piece.
        Doesn't take check into account.
        """
        #need to check for check
        if to_pos in self.list_moves():
            return True
        return False

    def verify_square(self, square):
        """
        Returns True if target square is valid for piece of certain color.
        """
        if not self._in_bounds(square):
            return False
        if not self.board.get(square): #empty
            return True
        if self.board[square].color != self.color: #enemy
            return True

    def empty_square(self, square):
        """
        Returns True if target square is valid and empty.
        """
        if not self._in_bounds(square):
            return False
        if self.board.get(square):
            return False
        return True

    def scan_direction(self, direction):
        """
        Finds valid squares in a direction

        Parameters:
            direction: tuple in form (x, y). Both int of -1, 0 or 1

        Returns:
            list of pos tuples (x, y) in a direction that are on the board
                and either empty or containing the first enemy piece
        """
        valid_moves = set()
        pos = (self.pos[0] + direction[0], self.pos[1] + direction[1])
        while self.empty_square(pos):
            valid_moves.add(pos)
            pos = (pos[0] + direction[0], pos[1] + direction[1])
        if self.verify_square(pos):
            valid_moves.add(pos)
        return valid_moves

    @staticmethod
    def _in_bounds(pos):
        """
        Returns True if target square on the board.
        """
        if pos[0] < 1 or pos[0] > 8 or pos[1] < 1 or pos[1] > 8:
            return False
        return True

class Pawn(Piece):
    def __init__(self, board, color, pos):
        super().__init__(board, color, pos)
        if color == WHITE:
            self.symbol = "P"
        elif color == BLACK:
            self.symbol = "p"

    def list_moves(self):
        valid_moves = set()
        if self.color == WHITE:
            color_direction = 1
            starting_row = 2
        elif self.color == BLACK:
            color_direction = -1
            starting_row = 7

        move_pos = (self.pos[0], self.pos[1] + color_direction)
        if not self.board.get(move_pos): #if space in front empty
            valid_moves.add(move_pos)
            #pawns can move double if not moved previously and empty
            if self.pos[1] == starting_row: 
                move_pos = (self.pos[0], self.pos[1] + 2*color_direction)
                if not self.board.get(move_pos):
                    valid_moves.add(move_pos)

        take_pos_tuple = ((self.pos[0] + 1, self.pos[1] + color_direction),
                          (self.pos[0] - 1, self.pos[1] + color_direction))
        for take_pos in take_pos_tuple:
            if self.board.get(take_pos):
                if self.board[take_pos].color != self.color:
                    valid_moves.add(take_pos)

        return valid_moves

class Rook(Piece):
    def __init__(self, board, color, pos):
        super().__init__(board, color, pos)
        self.has_moved = False
        if color == WHITE:
            self.symbol = "R"
        elif color == BLACK:
            self.symbol = "r"

    def list_moves(self):
        valid_moves = set()
        for direction in CARDINALS:
            valid_moves.update(self.scan_direction(direction))
        return valid_moves

class Knight(Piece):
    def __init__(self, board, color, pos):
        super().__init__(board, color, pos)
        if color == WHITE:
            self.symbol = "C"
        elif color == BLACK:
            self.symbol = "c"

    def list_moves(self):
        valid_moves = set()
        knight_moves = [
                (1, 2), (2, 1), (2, -1), (1, -2),
                (-1, -2), (-2, -1), (-2, 1), (-1, 2)
                ]
        for move in knight_moves:
            target_pos = (self.pos[0] + move[0], self.pos[1] + move[1])
            if self.verify_square(target_pos):
                valid_moves.add(target_pos)
        return valid_moves

class Bishop(Piece):
    def __init__(self, board, color, pos):
        super().__init__(board, color, pos)
        if color == WHITE:
            self.symbol = "B"
        elif color == BLACK:
            self.symbol = "b"

    def list_moves(self):
        valid_moves = set()
        for direction in DIAGONALS:
            valid_moves.update(self.scan_direction(direction))
        return valid_moves

class Queen(Piece):
    def __init__(self, board, color, pos):
        super().__init__(board, color, pos)
        if color == WHITE:
            self.symbol = "Q"
        elif color == BLACK:
            self.symbol = "q"

    def list_moves(self):
        valid_moves = set()
        for direction in (CARDINALS + DIAGONALS):
            valid_moves.update(self.scan_direction(direction))
        return valid_moves

class King(Piece):
    def __init__(self, board, color, pos):
        super().__init__(board, color, pos)
        self.has_moved = False
        if color == WHITE:
            self.symbol = "K"
        elif color == BLACK:
            self.symbol = "k"

    def list_moves(self):
        valid_moves = set()
        valid_moves.update(self.list_castling_moves())
        for direction in (CARDINALS + DIAGONALS):
            new_pos = (self.pos[0] + direction[0], self.pos[1] + direction[1])
            if self.verify_square(new_pos):
                valid_moves.add(new_pos)
        return valid_moves

    def list_castling_moves(self):
        castling_moves = set()
        if not self.has_moved:
            corner_pos = (1, self.pos[1])
            if (not self.board.get((2, self.pos[1])) and
                not self.board.get((3, self.pos[1])) and
                not self.board.get((4, self.pos[1])) and
                self.board.get(corner_pos)):
                if self.board[corner_pos].symbol in ("R", "r"):
                    if not self.board.get(self.pos[0], 1).has_moved:
                        castling_moves.add((3, self.pos[1]))
            corner_pos = (8, self.pos[1])
            if (not self.board.get((7, self.pos[1])) and
                not self.board.get((6, self.pos[1])) and
                self.board.get(corner_pos)):
                if self.board[corner_pos].symbol in ("R", "r"):
                    if not self.board.get(corner_pos).has_moved:
                        castling_moves.add((7, self.pos[1]))
        return castling_moves