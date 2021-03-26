# TODO Functions to test out whether things are implemented correctly.
from chess import ChessBoard
from chessMove import ChessMove
import unittest
import random
import pprint as pp

black = 'black'
white = 'white'

pawn = 'pawn'
rook = 'rook'
knight = 'knight'
bishop = 'bishop'
queen = 'queen'
king = 'king'

move_set = 'moves'
priority = 'priority'

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

class TestChess(unittest.TestCase):
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
        self.assertIn(((3, 1), (6, 1)), black_moves['rook0'], 'rook0 31 to 61 is in black moves.')

        white_moves = self.board_small.white_moves
        self.assertNotIn(((6, 1), (5, 2)), white_moves['pawn0'], 'pawn0 61 to 52 is not in white moves.')
    
    def test_board_big(self):
        self.setUp()

        board = self.board_big.board
        color = board[(0, 0)]['color']
        piece = board[(7, 3)]['name']
        self.assertEqual(color, black, 'Color should be black')
        self.assertEqual(piece[:-1], queen, 'Piece should be queen')

        black_moves = self.board_big.black_moves
        self.assertIn(((0, 2), (3, 5)), black_moves['bishop0'], 'bishop0 02 to 35 is in black moves.')
        
        white_moves = self.board_big.white_moves
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
        self.assertIn('queen0', small_board.white_moves, "queen0 should be in white moves before the move")
        self.assertFalse(small_board.board[(4, 2)]['name']=='bishop0', "Before move, bishop0 should not be in board position 42")

        moves = small_board.get_prioritized_moves(black)
        self.assertNotIn(((4, 2), (5, 1)), moves, "bishop0 42 to 51 is not in black moves before moving")

        move = ((5, 3), (4, 2))
        small_board._adjust_positions(move)
        self.assertNotIn('queen0', small_board.white_moves, "queen0 should not be in white moves after black's bishop0 53 to 42")
        self.assertTrue(small_board.board[(4, 2)]['name']=='bishop0', "After move, bishop0 should be in board position 42")

        moves = small_board.get_prioritized_moves(black)
        self.assertIn(((4, 2), (5, 1)), moves, "bishop0 42 to 51 is in black moves after moving")


if __name__ == '__main__':
    unittest.main()