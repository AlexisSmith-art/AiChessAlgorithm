import copy

black = 'black'
white = 'white'

pawn = 'pawn'
rook = 'rook'
knight = 'knight'
bishop = 'bishop'
queen = 'queen'
king = 'king'

class ChessMove():
    def __init__(self, color, board):
        self.color = color
        self.board = board


    def moves(self, piece, position):
        if piece == pawn:
            return self._pawn_moves(position)
        if piece == rook:
            return self._rook_moves(position)
        if piece == knight:
            return self._knight_moves(position)
        if piece == bishop:
            return self._bishop_moves(position)
        if piece == queen:
            return self._queen_moves(position)
        if piece == king:
            return self._king_moves(position)
    

    def occupied_squares(self, position):
        squares = set()
        increments = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

        for p in increments:
            x = position
            while True:
                square = self._math(x, p[0], p[1])
                if square not in self.board:
                    break
                if self.board[square]:
                    name = self.board[square]['name']
                    squares.add((name, square))
                    break
                else:
                    x = square

        possible_squares = [
            self._math(position, 2, 1),
            self._math(position, 1, 2),
            self._math(position, -1, 2),
            self._math(position, -2, 1),
            self._math(position, -2, -1),
            self._math(position, -1, -2),
            self._math(position, 1, -2),
            self._math(position, 2, -1),
        ]

        for square in possible_squares:
            if square not in self.board:
                continue
            if self.board[square]:
                name = self.board[square]['name']
                squares.add((name, square))
        
        return squares
    

    def _pawn_moves(self, position):
        moves = set()

        # Standard move
        move = self._math(position, 1)
        if move in self.board and not self.board[move]:
            moves.add((position, move))
        
        # Starting move
        block = move
        move = self._math(position, 2)
        if (self.color == white and position[0] == 6) or (self.color == black and position[0] == 1):
            if not self.board[move] and not self.board[block]:
                moves.add((position, move))

        # Capturing move
        positions = [self._math(position, 1, 1), self._math(position, 1, -1)]
        for move in positions:
            if move in self.board:
                if self.board[move] and self.board[move]['color'] != self.color:
                    moves.add((position, move))

        # print(self.color, ' Pawn @ ', position, ': ', moves)
        return moves
    

    def _rook_moves(self, position):
        moves = set()
        increments = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        
        # Standard moves
        for p in increments:
            x = position
            while True:
                move = self._math(x, p[0], p[1])
                if move not in self.board:
                    break
                if self.board[move] and self.board[move]['color'] == self.color:
                    break
                elif self.board[move] and self.board[move]['color'] != self.color:
                    moves.add((position, move))
                    break
                else:
                    moves.add((position, move))
                    x = move

        # print(self.color, ' Rook @ ', position, ': ', moves)
        return moves
    
    def _knight_moves(self, position):
        moves = set()

        # All possible moves
        possible_moves = [
            self._math(position, 2, 1),
            self._math(position, 1, 2),
            self._math(position, -1, 2),
            self._math(position, -2, 1),
            self._math(position, -2, -1),
            self._math(position, -1, -2),
            self._math(position, 1, -2),
            self._math(position, 2, -1),
            ]
        
        # Filter for moves that overlaps with own pieces.
        for move in possible_moves:
            if move not in self.board:
                continue
            if not self.board[move]:
                moves.add((position, move))
            elif self.board[move]['color'] != self.color:
                moves.add((position, move))

        # print(self.color, ' Knight @ ', position, ': ', moves)
        return moves
    
    def _bishop_moves(self, position):
        moves = set()
        increments = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        
        # Standard moves
        for p in increments:
            x = position
            while True:
                move = self._math(x, p[0], p[1])
                if move not in self.board:
                    break
                if self.board[move] and self.board[move]['color'] == self.color:
                    break
                elif self.board[move] and self.board[move]['color'] != self.color:
                    moves.add((position, move))
                    break
                else:
                    moves.add((position, move))
                    x = move
        
        # print(self.color, ' Bishop @ ', position, ': ', moves)
        return moves
    
    def _queen_moves(self, position):
        moves = set()
        increments = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
       
        # Standard moves
        for p in increments:
            x = position
            while True:
                move = self._math(x, p[0], p[1])
                if move not in self.board:
                    break
                if self.board[move] and self.board[move]['color'] == self.color:
                    break
                elif self.board[move] and self.board[move]['color'] != self.color:
                    moves.add((position, move))
                    break
                else:
                    moves.add((position, move))
                    x = move
        
        # print(self.color, ' Queen @ ', position, ': ', moves)
        return moves
    
    def _king_moves(self, position):
        moves = set()

        # All possible moves
        possible_moves = [
            self._math(position, 1, 0),
            self._math(position, 1, 1),
            self._math(position, 0, 1),
            self._math(position, -1, 1),
            self._math(position, -1, 0),
            self._math(position, -1, -1),
            self._math(position, 0, -1),
            self._math(position, 1, -1),
            ]

        # Filter for moves that overlaps with own pieces.
        for move in possible_moves:
            if move not in self.board:
                continue
            if not self.board[move]:
                moves.add((position, move))
            elif self.board[move]['color'] != self.color:
                moves.add((position, move))
        
        # print(self.color, ' King @ ', position, ': ', moves)
        return moves

    def _math(self, cell, x=0, y=0):
        if self.color == white:
            return((cell[0]-x, cell[1]+y))
        elif self.color == black:
            return((cell[0]+x, cell[1]-y))