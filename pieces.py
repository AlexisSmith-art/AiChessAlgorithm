class ChessPiece():
    def __init__(self, start, color, height, width):
        self.start = start 
        self.color = color
        self.position = start

        self.board = set()
        for row in range(height):
            for col in range(width):
                self.board.add((row, col))

    def _math(self, cell, x=0, y=0):
        if self.color == 'white':
            return((cell[0]-x, cell[1]+y))
        elif self.color == 'black':
            return((cell[0]+x, cell[1]+y))

class Pawn(ChessPiece):
    def __init__(self, start, color, height, width):
        super().__init__(start, color, height, width)
        self.symbol = '♙' if self.color == 'white' else '♟'

    def moves(self):
        moves = [self._math(self.position, 1)]
        if self.position == self.start:
            moves.append(self._math(self.start, 2))
        return [move for move in moves if move in self.board]

class Rook(ChessPiece):
    def __init__(self, start, color, height, width):
        super().__init__(start, color, height, width)
        self.symbol = '♖' if self.color == 'white' else '♜'

    def moves(self):
        moves = [
            cell for cell in self.board if 
            cell[0]==self.position[0] or cell[1]==self.position[1]
            ]
        return moves

class Knight(ChessPiece):
    def __init__(self, start, color, height, width):
        super().__init__(start, color, height, width)
        self.symbol = '♘' if self.color == 'white' else '♞'

    def moves(self):
        moves = [
            self._math(self.position, 2, 1),
            self._math(self.position, 2, -1),
            self._math(self.position, -2, 1),
            self._math(self.position, -2, -1),
            self._math(self.position, 1, 2),
            self._math(self.position, 1, -2),
            self._math(self.position, -1, 2),
            self._math(self.position, -1, -2),
            ]
        return [move for move in moves if move in self.board]

class Bishop(ChessPiece):
    def __init__(self, start, color, height, width):
        super().__init__(start, color, height, width)
        self.symbol = '♗' if self.color == 'white' else '♝'
        
    def moves(self):
        moves = [
            cell for cell in self.board if
            abs(cell[0] - self.position[0]) == abs(cell[1] - self.position[1])
            ]
        return moves

class Queen(ChessPiece):
    def __init__(self, start, color, height, width):
        super().__init__(start, color, height, width)
        self.symbol = '♕' if self.color == 'white' else '♛'
        
    def moves(self):
        moves = []
        for cell in self.board:
            if abs(cell[0] - self.position[0]) == abs(cell[1] - self.position[1]):
                moves.append(cell)
            elif cell[0]==self.position[0] or cell[1]==self.position[1]:
                moves.append(cell)
        return moves

class King(ChessPiece):
    def __init__(self, start, color, height, width):
        super().__init__(start, color, height, width)
        self.symbol = '♔' if self.color == 'white' else '♚'
        
    def moves(self):
        moves = [
            self._math(self.position, 1, 1),
            self._math(self.position, 1, -1),
            self._math(self.position, -1, 1),
            self._math(self.position, -1, -1),
            self._math(self.position, 1, 1),
            self._math(self.position, 1, -1),
            self._math(self.position, -1, 1),
            self._math(self.position, -1, -1),
            ]
        return [move for move in moves if move in self.board]
        