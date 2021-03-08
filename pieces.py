class ChessPiece():
    def __init__(self, start, color):
        self.start = start 
        self.color = color
        self.position = start

    def _math(self, cell, x=0, y=0):
        if self.color == 'white':
            return((cell[0]-x, cell[1]+y))
        elif self.color == 'black':
            return((cell[0]+x, cell[1]-y))

class Pawn(ChessPiece):
    def __init__(self, start, color):
        super().__init__(start, color)
        self.symbol = '♙' if self.color == 'white' else '♟'

    def moves(self, board):
        moves = []

        # Standard move
        position = self._math(self.position, 1)
        moves.append(position)
        
        # Starting move
        if self.position == self.start:
            moves.append(self._math(self.start, 2))
        
        moves = [move for move in moves if board[move[0]][move[1]] is None]

        # Capturing move
        positions = [self._math(self.position, 1, 1), self._math(self.position, 1, -1)]
        for move in positions:
            try:
                if board[move[0]][move[1]]:
                    if board[move[0]][move[1]].color != self.color:
                        moves.append(move)
            except IndexError:
                continue
        
        moves = [move for move in moves if move[0] >= 0 and move[1] >= 0]
        # print(self.color, ' Pawn @ ', self.position, ': ', moves)
        return moves

class Rook(ChessPiece):
    def __init__(self, start, color):
        super().__init__(start, color)
        self.symbol = '♖' if self.color == 'white' else '♜'

    def moves(self, board):
        moves = []
        increments = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        
        # Standard moves
        for p in increments:
            x = self.position
            while True:
                position = self._math(x, p[0], p[1])
                try:
                    if board[position[0]][position[1]] is None:
                        x = position
                        moves.append(position)
                    elif board[position[0]][position[1]].color != self.color:
                        moves.append(position)
                        break
                    else:
                        break
                except IndexError:
                    break
        
        moves = [move for move in moves if move[0] >= 0 and move[1] >= 0]
        # print(self.color, ' Rook @ ', self.position, ': ', moves)
        return moves

class Knight(ChessPiece):
    def __init__(self, start, color):
        super().__init__(start, color)
        self.symbol = '♘' if self.color == 'white' else '♞'

    def moves(self, board):
        moves = []

        # All possible moves
        possible_moves = [
            self._math(self.position, 2, 1),
            self._math(self.position, 1, 2),
            self._math(self.position, -1, 2),
            self._math(self.position, -2, 1),
            self._math(self.position, -2, -1),
            self._math(self.position, -1, -2),
            self._math(self.position, 1, -2),
            self._math(self.position, 2, -1),
            ]
        
        # Filter for moves that overlaps with own pieces.
        for move in possible_moves:
            try:
                if board[move[0]][move[1]] is None or board[move[0]][move[1]].color != self.color:
                    moves.append(move)
            except IndexError:
                continue
        
        moves = [move for move in moves if move[0] >= 0 and move[1] >= 0]
        # print(self.color, ' Knight @ ', self.position, ': ', moves)
        return moves

class Bishop(ChessPiece):
    def __init__(self, start, color):
        super().__init__(start, color)
        self.symbol = '♗' if self.color == 'white' else '♝'
        
    def moves(self, board):
        moves = []
        increments = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        
        # Standard moves
        for p in increments:
            x = self.position
            while True:
                position = self._math(x, p[0], p[1])
                try:
                    if board[position[0]][position[1]] is None:
                        x = position
                        moves.append(position)
                    elif board[position[0]][position[1]].color != self.color:
                        moves.append(position)
                        break
                    else:
                        break
                except IndexError:
                    break
        
        moves = [move for move in moves if move[0] >= 0 and move[1] >= 0]
        # print(self.color, ' Bishop @ ', self.position, ': ', moves)
        return moves

class Queen(ChessPiece):
    def __init__(self, start, color):
        super().__init__(start, color)
        self.symbol = '♕' if self.color == 'white' else '♛'
        
    def moves(self, board):
        moves = []
        increments = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
       
        # Standard moves
        for p in increments:
            x = self.position
            while True:
                position = self._math(x, p[0], p[1])
                try:
                    if board[position[0]][position[1]] is None:
                        x = position
                        moves.append(position)
                    elif board[position[0]][position[1]].color != self.color:
                        moves.append(position)
                        break
                    else:
                        break
                except IndexError:
                    break
        
        moves = [move for move in moves if move[0] >= 0 and move[1] >= 0]
        # print(self.color, ' Queen @ ', self.position, ': ', moves)
        return moves

class King(ChessPiece):
    def __init__(self, start, color):
        super().__init__(start, color)
        self.symbol = '♔' if self.color == 'white' else '♚'
        
    def moves(self, board):
        moves = []

        # All possible moves
        possible_moves = [
            self._math(self.position, 1, 0),
            self._math(self.position, 1, 1),
            self._math(self.position, 0, 1),
            self._math(self.position, -1, 1),
            self._math(self.position, -1, 0),
            self._math(self.position, -1, -1),
            self._math(self.position, 0, -1),
            self._math(self.position, 1, -1),
            ]

        # Filter for moves that overlaps with own pieces.
        for move in possible_moves:
            try:
                if board[move[0]][move[1]] is None or board[move[0]][move[1]].color != self.color:
                    moves.append(move)
            except IndexError:
                continue
        
        moves = [move for move in moves if move[0] >= 0 and move[1] >= 0]
        print(self.color, ' King @ ', self.position, ': ', moves)
        return moves
        