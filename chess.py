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

    pieces = {
        'white_pawn': '♙',
        'white_rook': '♖',
        'white_knight': '♘',
        'white_bishop': '♗',
        'white_queen': '♕',
        'white_king': '♔',
        'black_pawn': '♟',
        'black_rook': '♜',
        'black_knight': '♞',
        'black_bishop': '♝',
        'black_queen': '♛',
        'black_king': '♚',
    }

    def __init__(self, height=8, width=8, dict=start_arrangement):
        self.height = height
        self.width = width
        
        self.black = {}
        self.white = {}
        item_count = 0
        total_set = set()

        for key, value in dict.items():
            item_count += len(value)
            total_set.update(value)
            if 'white' in key:
                self.white[key.split('_')[1]] = value
            elif 'black' in key:
                self.black[key.split('_')[1]] = value
        
        if item_count != len(total_set):
            raise Exception('Duplicate starting positions found. Please correct and try again.')

        self.empty_spaces = set()
        for row in range(height):
            for col in range(width):
                if (row, col) not in total_set:
                    self.empty_spaces.add((row, col))
    
    def possible_moves(self, player):
        moves = []
        if player == 'white':
            for key, value in self.white:
                for cell in value:
                    moves.extend(self.__moves(key, cell))
        elif player == 'black':
            for key, value in self.black:
                for cell in value:
                    moves.extend(self.__moves(key, cell))
        return moves
    
    def __moves(self, piece, cell):
        pass
    
    def print_board(self, pieces=pieces):
        for x in [' ', 'A' , 'B', 'C', 'D', 'E', 'F', 'G', 'H', ' ']:
            print(f' {x} ', end='')
        print()
        for row in range(self.height):
            print(f' {row+1} ', end='')
            for col in range(self.width):
                added = False
                for key, val in self.black.items():
                    if (row, col) in val:
                        print(f"[{pieces[f'black_{key}']}]", end='')
                        added = True
                        break
                if added:
                    continue
                for key, val in self.white.items():
                    if (row, col) in val:
                        print(f"[{pieces[f'white_{key}']}]", end='')
                        added = True
                        break 
                if added:
                    continue
                if (row, col) in self.empty_spaces:
                    print('[•]', end='')
            print(f' {row+1} ', end='')
            print()
        for x in [' ', 'A' , 'B', 'C', 'D', 'E', 'F', 'G', 'H', ' ']:
            print(f' {x} ', end='')
        print()


board = ChessBoard()
board.print_board()
print(board.white)

