black = 'black'
white = 'white'
pawn = 'pawn'
rook = 'rook'
knight = 'knight'
bishop = 'bishop'
queen = 'queen'
king = 'king'

class ChessMove():
    def __init__(self, height, width, color, black_pieces, white_pieces):
        self.height = height
        self.width = width
        self.color = color
        self.black_positions = set()
        self.white_positions = set()

        for positions in black_pieces.values():
            self.black_positions.update(positions)
        
        for positions in white_pieces.values():
            self.white_positions.update(positions)
        
        self.positions = {
            black: self.black_positions,
            white: self.white_positions,
        }

        self.opposings = {
            black: self.white_positions,
            white: self.black_positions
        }


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


    def _pawn_moves(self, position):
        moves = []

        # Standard move
        move = self._math(position, 1)
        if move not in self.black_positions | self.white_positions:
            moves.append(move)
        
        # Starting move
        move = self._math(position, 2)
        block = self._math(position, 1)
        if (self.color == white and position[0] == 6) or (self.color == black and position[0] == 1):
            if (move and block) not in self.black_positions | self.white_positions:
                moves.append(move)

        # Capturing move
        positions = [self._math(position, 1, 1), self._math(position, 1, -1)]
        for move in positions:
            if move in self.opposings[self.color] and self._in_board(move):
                moves.append(move)

        # print(self.color, ' Pawn @ ', position, ': ', moves)
        return moves
    

    def _rook_moves(self, position):
        moves = []
        increments = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        
        # Standard moves
        for p in increments:
            x = position
            while True:
                move = self._math(x, p[0], p[1])
                if not self._in_board(move):
                    break
                if move in self.positions[self.color]:
                    break
                elif move in self.opposings[self.color]:
                    moves.append(move)
                    break
                else:
                    moves.append(move)
                    x = move

        # print(self.color, ' Rook @ ', position, ': ', moves)
        return moves
    
    
    def _knight_moves(self, position):
        moves = []

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
            if not self._in_board(move):
                continue
            if move not in self.black_positions | self.white_positions or move not in self.positions[self.color]:
                moves.append(move)

        # print(self.color, ' Knight @ ', position, ': ', moves)
        return moves
    

    def _bishop_moves(self, position):
        moves = []
        increments = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        
        # Standard moves
        for p in increments:
            x = position
            while True:
                move = self._math(x, p[0], p[1])
                if not self._in_board(move):
                    break
                if move in self.positions[self.color]:
                    break
                elif move in self.opposings[self.color]:
                    moves.append(move)
                    break
                else:
                    moves.append(move)
                    x = move
        
        # print(self.color, ' Bishop @ ', position, ': ', moves)
        return moves


    def _queen_moves(self, position):
        moves = []
        increments = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
       
        # Standard moves
        for p in increments:
            x = position
            while True:
                move = self._math(x, p[0], p[1])
                if not self._in_board(move):
                    break
                if move in self.positions[self.color]:
                    break
                elif move in self.opposings[self.color]:
                    moves.append(move)
                    break
                else:
                    moves.append(move)
                    x = move
        
        # print(self.color, ' Queen @ ', position, ': ', moves)
        return moves


    def _king_moves(self, position):
        moves = []

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
            if not self._in_board(move):
                continue
            if move not in self.black_positions | self.white_positions or move not in self.positions[self.color]:
                moves.append(move)
        
        # print(self.color, ' King @ ', position, ': ', moves)
        return moves

    def _math(self, cell, x=0, y=0):
        if self.color == white:
            return((cell[0]-x, cell[1]+y))
        elif self.color == black:
            return((cell[0]+x, cell[1]-y))
    
    def _in_board(self, move):
        if 0 <= move[0] < self.height and 0 <= move[1] < self.width:
            return True
        return False     