from chessMove import ChessMove

black = 'black'
white = 'white'
pawn = 'pawn'
rook = 'rook'
knight = 'knight'
bishop = 'bishop'
queen = 'queen'
king = 'king'

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

    def __init__(self, height=8, width=8, dict=start_arrangement2):
        self.height = height
        self.width= width
        self._black_pieces = {}
        self._white_pieces = {}

        for key, value in dict.items():
            color = key.split('_')[0]
            if color not in [black, white]:
                raise Exception(f"{key} is not valid. Please use {black} or {white} formatted as color_piece.")

            chessman = key.split('_')[1]
            if chessman not in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
                raise Exception(f"{key} is not valid. Please use 'pawn', 'rook', 'knight', 'bishop', 'queen', or 'king' formated as 'color_piece'.")

            if color == black:
                self._black_pieces[chessman] = value
            elif color == white:
                self._white_pieces[chessman] = value
    

    def possible_moves(self, player, black_pieces, white_pieces):
        all_moves = []
        chess_move = ChessMove(self.height, self.width, player, black_pieces, white_pieces)
        if player == white:
            for piece, positions in white_pieces.items():
                for position in positions:
                    moves = chess_move.moves(piece, position)
                    if moves:
                        for move in moves:
                            all_moves.append((position, move))
        elif player == black:
            for piece, positions in black_pieces.items():
                for position in positions:
                    moves = chess_move.moves(piece, position)
                    if moves:
                        for move in moves:
                            all_moves.append((position, move))
        return all_moves
                    

    def make_move(self, move, black_pieces, white_pieces):
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
    

    def evaluate(self, black_pieces, white_pieces):
        value = 0
        worth = {
            pawn: 1,
            rook: 5,
            knight: 3,
            bishop: 3,
            queen: 9,
            king: 0,
        }
        for piece, positions in black_pieces.items():
            value += worth[piece] * len(positions)
        for piece, positions in white_pieces.items():
            value -= worth[piece] * len(positions)
        return value

    
    def has_won(self, black_pieces, white_pieces):
        if not black_pieces[king]:
            return white
        elif not white_pieces[king]:
            return black
        else:
            return None
    
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
        board = self._generate_board(self._black_pieces, self._white_pieces)
        letters = ['0', '1', '2', '3', '4', '5', '6', '7']
        print(' ', end='')
        for letter in letters:
            print(f' {letter} ', end='')
        print()
        for index, row in enumerate(board):
            print("----" * self.width)
            print(index, end='')
            for cell in row:
                if cell:
                    print(f"|{symbols[cell]} ", end='')
                else:
                    print("|  ", end='')
            print("|", end='')
            print(index)
        print(' ', end='')
        for letter in letters:
            print(f' {letter} ', end='')
        print()
                    

    def _generate_board(self, black_pieces, white_pieces):
        board = []
        for i in range(self.height):
            row = []
            for i in range(self.width):
                row.append(None)
            board.append(row)

        for piece, positions in black_pieces.items():
            for position in positions:
                board[position[0]][position[1]] = f'{black}_{piece}'
        for piece, positions in white_pieces.items():
            for position in positions:
                board[position[0]][position[1]] = f'{white}_{piece}'
        return board


    def _set_positions(self, move):
        black_pieces, white_pieces = self.make_move(move, self._black_pieces, self._white_pieces)
        self._black_pieces = black_pieces
        self._white_pieces = white_pieces
    

    def _evaluate(self):
        return self.evaluate(self._black_pieces, self._white_pieces)
    

    def _has_won(self):
        return self.has_won(self._black_pieces, self._white_pieces)
    
    
board = ChessBoard()
board.print_board()
board.possible_moves(white, board._black_pieces, board._white_pieces)
'''
board._set_positions(((0, 4), (7, 5)))
print(board.black_pieces)
print(board.white_pieces)'''