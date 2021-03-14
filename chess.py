import pprint as pp
from chessMove import ChessMove
import copy
import random

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

worth = {
    pawn: 1,
    rook: 5,
    knight: 3,
    bishop: 3,
    queen: 9,
    king: 30,
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

    def __init__(self, height: int=8, width: int=8, dict=start_arrangement):
        if height > 8 or height < 1 or width > 8 or width < 1:
            print('Height and width must be an integer between 1-8, inclusive.')

        self.height = height
        self.width = width

        # Used to quickly locate information about a piece.
        self.board = {}
        # Used to save all possible moves at any given moment.
        self.black_moves = {}
        self.white_moves = {}

        black_pieces = set()
        white_pieces = set()
        for piece, positions in dict.items():
            for index, position in enumerate(positions):
                self.board[position] = {}
                color, name = piece.split('_')
                self.board[position]['name'] = name + str(index)
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
            moves = chess_move.moves(name[:-1], point)
            moves = [{move_set: move, priority: 0} for move in moves]
            self.black_moves[name] = moves
        
        chess_move = ChessMove(white, self.board)
        for point in white_pieces:
            piece = self.board[point]
            name = piece['name']
            moves = chess_move.moves(name[:-1], point)
            moves = [{move_set: move, priority: 0} for move in moves]
            self.white_moves[name] = moves


    # Adjusts all the stored class variables after a move. Returns nothing.
    def _adjust_positions(self, choice):
        self.black_moves, self.white_moves, self.board = self.adjust_positions(choice, self.black_moves, self.white_moves, self.board)


    # Returns a new set of moves and updated board as a result of a move. Does not change the stored class variables. For use in minimax.
    def adjust_positions(self, move, black_moves, white_moves, board):
        previous_position = move[0]
        new_position = move[1]
        black_moves = copy.deepcopy(black_moves)
        white_moves = copy.deepcopy(white_moves)
        board = copy.deepcopy(board)
        same_moves = {
            black: black_moves,
            white: white_moves,
        }

        # In moves, remove all moves belonging to the piece that moved.
        color = board[previous_position]['color']
        name = board[previous_position]['name']
        same_moves[color][name].clear()

        # In moves, if a piece was at the new square, remove that piece from the dictionary.
        if board[new_position]:
            color = board[new_position]['color']
            name = board[new_position]['name']
            same_moves[color].pop(name)

        # In board, change the board so that the piece moves to a new location.
        info = board[previous_position]
        board[new_position] = info
        board[previous_position] = None

        # Add new moves for the moved piece.
        color = board[new_position]['color']
        name = board[new_position]['name']
        chess_move = ChessMove(color, board)
        moves = chess_move.moves(name[:-1], new_position)
        moves = [{move_set: move, 'priority': 0} for move in moves]
        same_moves[color][name].extend(moves)

        # Clear all moves of pieces affected by the move, and then add the updated moves.
        squares = chess_move.occupied_squares(new_position)
        for square in squares:
            name = square[0]
            position = square[1]
            color = board[position]['color']
            same_moves[color][name].clear()
            chess_move.color = color
            moves = chess_move.moves(name[:-1], position)
            moves = [{move_set: move, priority: 0} for move in moves]
            same_moves[color][name].extend(moves)
        
        return black_moves, white_moves, board


    # TODO check if the board is in checkmate or check
    def check(self, player, black_pieces, white_pieces):
        raise NotImplementedError


    # Returns the value of a given board. Currently needs to smartly consider checks and checkmates. For use in minimax.
    # Need to be a lot more effective by not skipping moves that leads to sure wins.
    def evaluate(self, board):
        value = 0
        for info in board.values():
            if info:
                color = info['color']
                if color == black:
                    value += worth[info['name'][:-1]]
                elif color == white:
                    value -= worth[info['name'][:-1]]
        return value
    

    # Returns the player that won if there is one, otherwise None. For use in minimax. 
    def has_won(self, black_moves, white_moves):
        if 'king0' not in white_moves:
            return black
        elif 'king0' not in black_moves:
            return white
        else:
            return None


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
                    print(f'|{symbols[cell[:-1]]} ', end='')
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
chess_board.print_board()
pp.pprint(chess_board.black_moves)
pp.pprint(chess_board.white_moves)
all_white_moves = []
for value in chess_board.white_moves.values():
    for dict in value:
        moves = dict[move_set]
        all_white_moves.append(moves)
move = random.choice(all_white_moves)
black_moves, white_moves, board = chess_board.adjust_positions(move, chess_board.black_moves, chess_board.white_moves, chess_board.board)
chess_board.board = board
chess_board.print_board()
pp.pprint(black_moves)
pp.pprint(white_moves)'''