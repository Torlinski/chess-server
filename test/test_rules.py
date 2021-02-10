from src.chess_server.engine import BLACK, WHITE, CARDINALS, DIAGONALS
from src.chess_server.engine import Board, Pawn, Rook, Knight, Bishop, Queen, King, Piece

board = Board()

def test_pretty_board():
    pretty_board = board.display_board()
    target_pretty_board = (
"""    a   b   c   d   e   f   g   h
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
""")
    assert pretty_board == target_pretty_board

def test_32_pieces_exist():
    assert len(board.board) == 32

def test_knight_valid_moves():
    white_knight = Knight(board.board, WHITE, (2, 5))
    valid_moves = white_knight.list_moves()
    assert valid_moves == {(4, 4), (3, 7), (4, 6), (1, 7), (3, 3), (1, 3)}

def test_piece_verify_move():
    white_knight = Knight(board.board, WHITE, (2, 5))
    assert white_knight.verify_move((3, 7))

def test_pawn_single_or_double_move():
    pawn = Pawn(board.board, WHITE, (4, 2))
    valid_moves = pawn.list_moves()
    assert valid_moves == {(4, 3), (4, 4)}

def test_pawn_take():
    pawn = Pawn(board.board, WHITE, (4, 6))
    valid_moves = pawn.list_moves()
    assert valid_moves == {(3, 7), (5, 7)}

def test_scan():
    rook = Piece(board.board, WHITE, (2, 3))
    upwards_scan = rook.scan_direction((0, 1))
    assert upwards_scan == {(2, 4), (2, 5), (2, 6), (2, 7)}

def test_rook():
    rook = Rook(board.board, WHITE, (4, 6))
    valid_moves = rook.list_moves()
    assert valid_moves == {(4, 4), (4, 3), (4, 5), (7, 6), (2, 6), (5, 6),
                           (8, 6), (3, 6), (6, 6), (1, 6), (4, 7)}

def test_bishop():
    bishop = Bishop(board.board, WHITE, (4, 6))
    valid_moves = bishop.list_moves()
    assert valid_moves == {(2, 4), (5, 5), (3, 5), (3, 7), (1, 3), (6, 4),
                           (5, 7), (7, 3)}

def test_queen():
    queen = Queen(board.board, WHITE, (4, 6))
    valid_moves = queen.list_moves()
    assert valid_moves == {(4, 4), (4, 3), (4, 5), (7, 6), (2, 6), (5, 6),
        (8, 6), (3, 6), (6, 6), (1, 6), (4, 7), (2, 4), (5, 5), (3, 5),
        (3, 7), (1, 3), (6, 4), (5, 7), (7, 3)}

def test_king_without_check():
    king = King(board.board, WHITE, (5, 3))
    valid_moves = king.list_moves()
    assert valid_moves == {(4, 4), (4, 3), (5, 4), (6, 4), (6, 3)}

def test_move_piece():
    board.move_piece((5, 2), (5, 4))
    print(board.display_board())
    assert board.board[(5, 4)].symbol == 'P'
    assert not board.board.get((5, 2))

def test_move_wrong_color():
    assert not board.move_piece((5, 4), (5, 5))

def test_move_exposing_king():
    board.move_piece((1, 7), (1, 6))
    board.move_piece((6, 1), (2, 5))
    print(board.display_board())
    board.move_piece((4, 7), (4, 6))
    print(board.display_board())
    assert board.board[(4, 7)].symbol == 'p'
    assert not board.board.get((4, 6))

def test_move_checks_opponent():
    board.move_piece((6, 7), (6, 6))
    board.move_piece((4, 1), (8, 5))
    print(board.move_history)
    print(board.display_board())
    assert board.move_history[-1][4] #looks at last move in history and sees if check

def test_move_king_into_check():
    board.move_piece((5, 8), (6, 7))
    print(board.display_board())
    assert board.board[(5, 8)].symbol == 'k'

def test_move_to_shield_king():
    board.move_piece((7, 7), (7, 6))
    print(board.display_board())
    assert board.board[(7, 6)].symbol == 'p'

def test_castling():
    board.move_piece((7, 1), (6, 3))
    board.move_piece((5, 7), (5, 5))
    board.move_piece((5, 1), (7, 1))
    print(board.display_board())
    assert board.board[(7, 1)].symbol == 'K'
    assert board.board[(6, 1)].symbol == 'R'
