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

        self.white = []
        self.black = []

        for key, value in dict.items():
            for cell in value:
                item_count += 1
                total_set.add(cell)
                color = key.split('_')[0]
                chessman = key.split('_')[1]
                piece = functions[chessman](cell, color, self.height, self.width)
                self.board[cell[0]][cell[1]] = piece
                if color == 'white':
                    self.white.append(piece)
                else:
                    self.black.append(piece)
                    
        if item_count != len(total_set):
            raise Exception('Duplicate starting positions found. Please correct and try again.')
    

    def possible_moves(self, player):
        moves = []
        if player == 'white':
            for piece in self.white:
                for move in piece.moves():
                    cell = self.board[move[0]][move[1]]
                    if not cell:
                        moves.append((piece.symbol, piece.position, move))
                    elif cell.color == 'black':
                        moves.append((piece.symbol, piece.position, move))
        elif player == 'black':
            for piece in self.black:
                for move in piece.moves():
                    cell = self.board[move[0]][move[1]]
                    if not cell:
                        moves.append((piece.symbol, piece.position, move))
                    elif cell.color == 'white':
                        moves.append((piece.symbol, piece.position, move))
        return moves
    

    def print_board(self):
        letters = ['0', '1', '2', '3', '4', '5', '6', '7']
        print(' ', end='')
        for letter in letters:
            print(f' {letter} ', end='')
        print()
        for row in range(self.height):
            print("----" * self.width)
            print(row, end='')
            for col in range(self.width):
                cell = self.board[row][col]
                if cell:
                    print(f"|{cell.symbol} ", end='')
                else:
                    print("|  ", end='')
            print("|", end='')
            print(row)
        print(' ', end='')
        for letter in letters:
            print(f' {letter} ', end='')
        print()


board = ChessBoard()
board.print_board()
print(board.possible_moves('white'))

