# TODO Functions to test out whether things are implemented correctly.
from chess import ChessBoard
from chessMove import ChessMove
import unittest
import random

black = 'black'
white = 'white'

pawn = 'pawn'
rook = 'rook'
knight = 'knight'
bishop = 'bishop'
queen = 'queen'
king = 'king'

test_small = {
    'white_pawn': {(6, 1)},
    'white_queen': {(4, 2)},
    'white_king': {(7, 0)},
    'black_rook': {(3, 1)},
    'black_bishop': {(5, 3)},
    'black_king': {(3, 2)},
}

test_big = {
        'black_pawn': {(4, int) for int in range(8)},
        'black_rook': {(0, 0), (0, 7)},
        'black_knight': {(0, 1), (0, 6)},
        'black_bishop': {(0, 2), (0, 5)},
        'black_queen': {(0, 3)},
        'black_king': {(0, 4)},
        'white_pawn': {(5, int) for int in range(8)},
        'white_rook': {(7, 0), (7, 7)},
        'white_knight': {(7, 1), (7, 6)},
        'white_bishop': {(7, 2), (7, 5)},
        'white_queen': {(7, 3)},
        'white_king': {(7, 4)},
    }

class TestSum(unittest.TestCase):
    def setUp(self): 
        self.board_small = ChessBoard(8, 4, dict=test_small)
        self.board_big = ChessBoard(dict=test_big)

    def test_board_small(self):
        self.setUp()

        board = self.board_small.board
        color = board[(6, 1)]['color']
        piece = board[(3, 1)]['name']
        self.assertEqual(color, white, 'Color should be white.')
        self.assertEqual(piece[:-1], rook, 'Piece should be rook.')

        black_moves = self.board_small.black_moves
        white_moves = self.board_small.white_moves
        self.assertIn(((3, 1), (6, 1)), black_moves['rook0'], 'rook0 31 to 61 is in black moves.')
        self.assertNotIn(((6, 1), (5, 2)), white_moves['pawn0'], 'pawn0 61 to 52 is not in white moves.')
    
    def test_board_big(self):
        self.setUp()

        board = self.board_big.board
        color = board[(0, 0)]['color']
        piece = board[(7, 3)]['name']
        self.assertEqual(color, black, 'Color should be black')
        self.assertEqual(piece[:-1], queen, 'Piece should be queen')

        black_moves = self.board_big.black_moves
        white_moves = self.board_big.white_moves
        self.assertIn(((0, 2), (3, 5)), black_moves['bishop0'], 'bishop0 02 to 35 is in black moves.')
        self.assertNotIn(((7, 6), (6, 4)), white_moves['knight1'], 'knight1 76 to 63 is not in white moves.')
    
    def test_evaluate(self):
        self.setUp()

        small_board = self.board_small
        value_small = small_board.evaluate(small_board.board)
        self.assertTrue(value_small != 0, 'Small board value should not be 0.')

        big_board = self.board_big
        value_big = big_board.evaluate(big_board.board)
        self.assertTrue(value_big == 0, 'Big board value should be 0.')
    
    def test_adjust_positions(self):
        self.setUp()

        small_board = self.board_small
        small_board.print_board()
        move = ((5, 3), (4, 2))
        black_moves, white_moves, board = small_board.adjust_positions(move, small_board.black_moves, small_board.white_moves, small_board.board)
        small_board.board = board
        small_board.print_board()
        print(white_moves)

if __name__ == '__main__':
    unittest.main()