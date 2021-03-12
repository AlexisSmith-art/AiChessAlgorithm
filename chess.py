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

worth = {
    pawn: 1,
    rook: 5,
    knight: 3,
    bishop: 3,
    queen: 9,
    king: 0,
}

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
    }

    def __init__(self, height=8, width=8, dict=start_arrangement):
        self.height = height
        self.width = width

        # Used to quickly locate information about a piece.
        self.board = {}
        # Used to save all possible moves at any given moment.
        self.black_moves = set()
        self.white_moves = set()
        self.same_moves = {
            black: self.black_moves,
            white: self.white_moves,
        }
        self.diff_moves = {
            black: self.white_moves,
            white: self.black_moves,
        }


        black_pieces = set()
        white_pieces = set()
        for piece, positions in dict.items():
            for position in positions:
                self.board[position] = {}
                color, name = piece.split('_')
                self.board[position]['name'] = name
                self.board[position]['color'] = color
                if color == black:
                    black_pieces.add(position)
                elif color == white:
                    white_pieces.add(position)

        for row in range(self.height):
            for col in range(self.width):
                if (row, col) not in self.board:
                    self.board[(row, col)] = None
        
        chess_move = ChessMove(black, self.board)
        for point in black_pieces:
            piece = self.board[point]
            name = piece['name']
            self.black_moves.update(chess_move.moves(name, point))
        
        chess_move = ChessMove(white, self.board)
        for point in white_pieces:
            piece = self.board[point]
            name = piece['name']
            self.white_moves.update(chess_move.moves(name, point))


    # TODO Adjusts all the stored class variables after a move. Returns nothing. Still need to smartly update the moves of the moved piece as well as all affected pieces.
    def _adjust_positions(self, choice):
        previous = choice[0]
        new = choice[1]
        name = self.board[previous]['name']
        color = self.board[previous]['color']

        # Updates self.all_moves
        for move in copy.deepcopy(self.same_moves[color]):
            if move[0] == previous:
                self.same_moves[color].remove(move)
        chess_move = ChessMove(color, self.board)
        self.same_moves[color].update(chess_move.moves(name, new))

        # Updates self.board
        info = self.board[previous]
        piece_present = copy.deepcopy(self.board[new])
        self.board[new] = info
        self.board[previous] = None


    def adjacent_squares(self, color, position):
        squares = []
        increments = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

        chess_move = ChessMove

        possible_squares = [
            ChessMove(color=color)._math(position, 2, 1),
            ChessMove(color=color)._math(position, 1, 2),
            ChessMove(color=color)._math(position, -1, 2),
            ChessMove(color=color)._math(position, -2, 1),
            ChessMove(color=color)._math(position, -2, -1),
            ChessMove(color=color)._math(position, -1, -2),
            ChessMove(color=color)._math(position, 1, -2),
            ChessMove(color=color)._math(position, 2, -1),
            ]


    # TODO Returns the result of making a move. Very similiar to _adjust_positions. Does not change the stored class variables. For use in minimax. Must return a new set of all possible moves (for next loop in the recursion)
    def adjust_positions(self, move, black_moves, white_moves, board):
        previous_position = move[0]
        new_position = move[1]
        board = copy.deepcopy(board)
        black_moves = copy.deepcopy(black_moves)
        white_moves = copy.deepcopy(white_moves)
        same_moves = {
            black: black_moves,
            white: white_moves,
        }

        # Remove all moves belonging to the piece that moved.
        color = board[previous_position]['color']
        same_moves[color] = {move for move in same_moves[color] if move[0] != previous_position}

        # If a piece was at the new square, remove all moves with that piece.
        if board[new_position]:
            color = board[new_position]['color']
            same_moves[color] = {move for move in same_moves[color] if move[0] != new_position}

        # Change the board so that the piece moves to a new location.
        info = board[previous_position]
        board[new_position] = info
        board[previous_position] = None

        # Remove all moves affected by the new location. Perhaps it is easiest find all the pieces that are 'close' to the moved piece before proceeding.
        color = board[new_position['color']]
        squares = self.adjacent_squares(color, new_position)
        

        # Check for adjacent pawns

        # Add new moves that can be made.
        
        # Find all other squares affected by the new location and check if a piece is there. If so, adjust the set of moves accordingly.



    # TODO check if the board is in checkmate or check
    def check(self, player, black_pieces, white_pieces):
        raise NotImplementedError


    # Returns the value of a given board. Currently needs to smartly consider checks and checkmates. For use in minimax.
    def evaluate(self, board):
        value = 0
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


    # Prints the current board.
    def print_board(self):
        board = [[None for i in range(self.width)] for j in range(self.height)]
        for square, info in self.board.items():
            row = square[0]
            col = square[1]
            if info:
                board[row][col] = f"{info['color']}_{info['name']}"

        print(' ', end='')
        for i in range(self.width):
            print(f' {letters[i]} ', end='')
        print()
        for index, row in enumerate(board):
            print('----' * self.width)
            print(index, end='')
            for cell in row:
                if cell:
                    print(f'|{symbols[cell]} ', end='')
                else:
                    print('|  ', end='')
            print(f'|{index}')
        print('----' * self.width)
        print(' ', end='')
        for i in range(self.width):
            print(f' {letters[i]} ', end='')
        print()
        
        
        
'''
chess_board = ChessBoard()
chess_board.print_board()'''