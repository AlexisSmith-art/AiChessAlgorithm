from pieces import *

class ChessBoard():
    
    start_arrangement = {
        'white_pawn': {(6, int) for int in range(8)},
        'white_rook': {(7, 0), (7, 7)},
        'white_knight': {(7, 1), (7, 6)},
        'white_bishop': {(7, 2), (7, 5)},
        'white_queen': {(7, 3)},
        'white_king': {(7, 4)},
        'black_pawn': {(1, int) for int in range(8)},
        'black_rook': {(0, 0), (0, 7)},
        'black_knight': {(0, 1), (0, 6)},
        'black_bishop': {(0, 2), (0, 5)},
        'black_queen': {(0, 3)},
        'black_king': {(0, 4)},
    }
    
    # Test
    start_arrangement2 = {
        'white_pawn': {(6, int) for int in range(8)},
        'white_rook': {(7, 0), (7, 7)},
        'white_knight': {(7, 1), (7, 6)},
        'white_bishop': {(7, 2), (7, 5)},
        'white_queen': {(7, 3)},
        'white_king': {(7, 4)},
        'black_pawn': {(5, int) for int in range(8)},
        'black_rook': {(0, 0), (0, 7)},
        'black_knight': {(0, 1), (0, 6)},
        'black_bishop': {(0, 2), (0, 5)},
        'black_queen': {(0, 3)},
        'black_king': {(0, 4)},
    }

    def __init__(self, height=8, width=8, dict=start_arrangement):
        self.height = height
        self.width = width

        # Create a board with all empty squares.
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(None)
            self.board.append(row)

        item_count = 0
        total_set = set()

        functions = {
            'pawn': Pawn,
            'rook': Rook,
            'knight': Knight,
            'bishop': Bishop,
            'queen': Queen,
            'king': King,
        }

        self.white = set()
        self.black = set()

        for key, value in dict.items():
            for cell in value:
                item_count += 1
                total_set.add(cell)

                color = key.split('_')[0]
                if color not in ['black', 'white']:
                    raise Exception(f"{key} is not valid. Please format as 'color_piece'.")

                chessman = key.split('_')[1]
                if chessman not in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
                    raise Exception(f"{key} is not valid. Please format as 'color_piece'.")

                piece = functions[chessman](cell, color)
                self.board[cell[0]][cell[1]] = piece
                if color == 'white':
                    self.white.add(piece)
                else:
                    self.black.add(piece)
                    
        if item_count != len(total_set):
            raise Exception('Duplicate starting positions found. Please correct and try again.')
    

    def possible_moves(self, player):
        moves = []
        if player == 'white':
            for piece in self.white:
                for move in piece.moves(self.board):
                    cell = self.board[move[0]][move[1]]
                    if not cell:
                        moves.append((piece.position, move))
                    elif cell.color == 'black':
                        moves.append((piece.position, move))
        elif player == 'black':
            for piece in self.black:
                for move in piece.moves(self.board):
                    cell = self.board[move[0]][move[1]]
                    if not cell:
                        moves.append((piece.position, move))
                    elif cell.color == 'white':
                        moves.append((piece.position, move))
        return moves
    

    def make_move(self, move):
        board = self.board.copy()
        start = move[0]
        end = move[1]
        piece = board[start[0]][start[1]]
        piece.position = end
        if board[end[0]][end[1]]:
            opponent_piece = board[end[0]][end[1]]
            opponent_piece.position = None
            color = opponent_piece.color
            if color == 'white':
                self.white.remove(opponent_piece)
            elif color == 'black':
                self.black.remove(opponent_piece)
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = None
        return board

    
    def evaluate(self, board):
        value = 0
        for row in board:
            for cell in row:
                if cell:
                    if cell.color == 'white':
                        value += cell.value
                    elif cell.color =='black':
                        value -= cell.value
        return value
    

    def has_won(self, board):
        white_king = False
        black_king = False
        for piece in self.white:
            if type(piece).__name__ == 'King':
                white_king = True
        
        for piece in self.black:
            if type(piece).__name__ == 'King':
                black_king = True
        
        if not black_king:
            return 'white'
        elif not white_king:
            return 'black'
        else:
            return None

    
    def translate(self, move):
        pass


    def print_board(self, board):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        print(' ', end='')
        for letter in letters:
            print(f' {letter} ', end='')
        print()
        for row in range(self.height):
            print("----" * self.width)
            print(row + 1, end='')
            for col in range(self.width):
                cell = board[row][col]
                if cell:
                    print(f"|{cell.symbol} ", end='')
                else:
                    print("|  ", end='')
            print("|", end='')
            print(row + 1)
        print(' ', end='')
        for letter in letters:
            print(f' {letter} ', end='')
        print()

'''
import random

board = ChessBoard()
board.print_board(board.board)
board.possible_moves('black')
print(board.has_won(board.board))


for i in range(300):
    if i % 2 == 0:
        move = random.choice(board.possible_moves('white'))
    else:
        move = random.choice(board.possible_moves('black'))
    new_board = board.make_move(move)
    board.print_board(new_board)
    value = board.evaluate(new_board)
    print(board.has_won(new_board))
    print(f'Move {move} caused the board to be worth {value}')'''