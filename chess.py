import pprint as pp
from chessMove import ChessMove
import copy

black = 'black'
white = 'white'

pawn = 'pawn'
rook = 'rook'
knight = 'knight'
bishop = 'bishop'
queen = 'queen'
king = 'king'

letters = ['0', '1', '2', '3', '4', '5', '6', '7']

class ChessBoard():

    start_arrangement = {
        'black_pawn': {(1, int) for int in range(8)},
        'black_rook': {(0, 0), (0, 7)},
        'black_knight': {(0, 1), (0, 6)},
        'black_bishop': {(0, 2), (0, 5)},
        'black_queen': {(0, 3)},
        'black_king': {(0, 4)},
        'white_pawn': {(6, int) for int in range(8)},
        'white_rook': {(7, 0), (7, 7)},
        'white_knight': {(7, 1), (7, 6)},
        'white_bishop': {(7, 2), (7, 5)},
        'white_queen': {(7, 3)},
        'white_king': {(7, 4)},

    test_small = {
        'white_pawn': {(6, int) for int in range(4)},
        'white_rook': {(7, 0)},
        'white_bishop': {(7, 3)},
        'white_queen': {(7, 1)},
        'white_king': {(7, 2)},
        'black_pawn': {(1, int) for int in range(4)},
        'black_rook': {(0, 0)},
        'black_bishop': {(0, 3)},
        'black_queen': {(0, 1)},
        'black_king': {(0, 2)},
    }

    def __init__(self, height, width, dict=test_small):
        self.height = height
        self.width = width

        # Used for calculating whether moves conflict due an occupied square. Also contains all pieces.
        self.black_pieces = set()
        self.white_pieces = set()
        self.same_pieces = {
            black: self.black_pieces,
            white: self.white_pieces,
        }
        self.diff_pieces = {
            black: self.white_pieces,
            white: self.black_pieces,
        }
        # Used to quickly locate information about a piece.
        self.board = {}
        # Used to save all possible moves at any given moment.
        self.all_moves = set()

        for piece, positions in dict.items():
            for position in positions:
                self.board[position] = {}
                color, name = piece.split('_')
                self.board[position]['name'] = name
                self.board[position]['color'] = color
                self.same_pieces[color].add(position)

        for row in range(self.height):
            for col in range(self.width):
                if (row, col) not in self.board:
                    self.board[(row, col)] = None
        
        chess_move = ChessMove(black, self.same_pieces, self.diff_pieces, self.board)
        for point in self.black_pieces:
            piece = self.board[point]
            name = piece['name']
            self.all_moves.update(chess_move.moves(name, point))
        
        chess_move = ChessMove(white, self.same_pieces, self.diff_pieces, self.board)
        for point in self.white_pieces:
            piece = self.board[point]
            name = piece['name']
            self.all_moves.update(chess_move.moves(name, point))


    # Adjusts all the stored class variables after a move. Returns nothing.
    def _adjust_positions(self, choice):
        previous = choice[0]
        new = choice[1]
        name = self.board[previous]['name']
        color = self.board[previous]['color']

        # Updates self.all_moves
        all_moves = copy.deepcopy(self.all_moves)
        for move in self.all_moves:
            if move[0] == previous:
                all_moves.remove(move)
        chess_move = ChessMove(color, self.same_pieces, self.diff_pieces, self.board)
        all_moves.update(chess_move.moves(name, new))
        self.all_moves = all_moves

        # Updates self.board
        info = self.board[previous]
        piece_present = copy.deepcopy(self.board[new])
        self.board[new] = info
        self.board[previous] = None

        # Updates self.black_pieces and self.white_pieces
        self.same_pieces[color].remove(previous).add(new)
        if piece_present:
            self.same_pieces[piece_present[new]['color']].remove(new)


    # TODO Returns the result of making a move. Very similiar to _adjust_positions. Does not change the stored class variables. For use in minimax.
    def adjust_positions(self, move, black_pieces, white_pieces):
        black_pieces = copy.deepcopy(black_pieces)
        white_pieces = copy.deepcopy(white_pieces)
        previous = move[0]
        current = move[1]
        for b_piece, b_positions in black_pieces.items():
            if previous in b_positions:
                black_pieces[b_piece].remove(previous)
                black_pieces[b_piece].add(current)
            elif current in b_positions:
                black_pieces[b_piece].remove(current)
        
        for w_piece, w_positions in white_pieces.items():
            if previous in w_positions:
                white_pieces[w_piece].remove(previous)
                white_pieces[w_piece].add(current)
            elif current in w_positions:
                white_pieces[w_piece].remove(current)
        return black_pieces, white_pieces


    # TODO check if the board is in checkmate or check
    def check(self, player, black_pieces, white_pieces):
        raise NotImplementedError


    # Returns the value of a given board. Currently needs to smartly consider checks and checkmates. For use in minimax.
    def evaluate(self, board):
        value = 0
        worth = {
            pawn: 1,
            rook: 5,
            knight: 3,
            bishop: 3,
            queen: 9,
            king: 35,
        }
        for info in board.values():
            if info:
                color = info['color']
                if color == black:
                    value += worth[info['name']]
                elif color == white:
                    value -= worth[info['name']]
        return value
 

    # TODO this function should NOT redo all possible moves every time a new board is present.
    # A change of one move, does not greatly change the moves possible.
    # This function should never adjust it's variables, but make copies of them.
    def possible_moves(self, player, black_pieces, white_pieces):
        raise NotImplementedError


    # TODO Still requires a smart way to print the board
    def print_board(self):
        symbols = {
            f'{black}_{pawn}': '♟',
            f'{black}_{rook}': '♜',
            f'{black}_{knight}': '♞',
            f'{black}_{bishop}': '♝',
            f'{black}_{queen}': '♛',
            f'{black}_{king}': '♚',
            f'{white}_{pawn}': '♙',
            f'{white}_{rook}': '♖',
            f'{white}_{knight}': '♘',
            f'{white}_{bishop}': '♗',
            f'{white}_{queen}': '♕',
            f'{white}_{king}': '♔',
        }
        print(' ', end='')
        for i in range(self.width):
            print(f' {letters[i]} ', end='')
        print()
        
        # TODO Some voodoo magic to make this work.

        for i in range(self.width):
            print(f' {letters[i]} ', end='')
        print()
        
        
        

chess_board = ChessBoard(8, 4)
pp.pprint(chess_board.board)
pp.pprint(chess_board.same_pieces)