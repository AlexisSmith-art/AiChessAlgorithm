from chess import ChessBoard
import math
import random
import copy

black = 'black'
white = 'white'
script_player = "Do you want to be the white or black player?"
script_player_error = "I'm sorry. Please enter white or black."
script_move = "Please choose a move below."
script_move_error = "Move must be an integer. For example, '2'."

# Test
test_large = {
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

# Test (height=8, width=4)
test_small = {
    'white_pawn': {(6, int) for int in range(4)},
    'white_rook': {(7, 0)},
    'white_bishop': {(7, 3)},
    'white_queen': {(7, 1)},
    'white_king': {(7, 2)},
    'black_pawn': {(1, int) for int in range(4)},
    'black_rook': {(0, 0)},
    'black_bishop': {(0, 3)},
    'black_queen': {(0, 1)},
    'black_king': {(0, 2)},
}

class ChessAI(ChessBoard):
    def play(self):
        print(script_player)
        response = input()
        while response != white and response != black:
            print(script_player_error)
            response = input()
        player = response
        ai = black if response == white else white
        print(f'player is: {player}, ai is: {ai}')
        self.print_board()

        while True:
            #print(script_move)
            possible_moves = self.possible_moves(player, self._black_pieces, self._white_pieces)
            #for index, move in enumerate(possible_moves):
            #    print(f'Move {index}: {move}')
            #response = '15'
            #while not response.isnumeric():
            #    print(script_move_error)
            #    response = input()
            player_move = random.choice(possible_moves)

            self.print_board()
            black_pieces, white_pieces = self.make_move(player_move, self._black_pieces, self._white_pieces)
            value = self.evaluate(black_pieces, white_pieces)
            print(f'{player} {player_move} has a value of {value}')
            self._set_positions(player_move)

            self.print_board()
            ai_move = self.best_move(self._black_pieces, self._white_pieces, 3, ai)
            self._set_positions(ai_move)

            if self._has_won():
                break
        
        self.print_board()
        print(f'The winner is: {self._has_won()}')

    # depth-limited minimax with alpha-beta pruning
    def minimax(self, black_moves, white_moves, board, depth, alpha, beta, player):
        if depth == 0 or self.has_won(black_pieces, white_pieces):
            return self.evaluate(black_pieces, white_pieces)
        
        if player == black:
            value = -math.inf
            all_black_moves = set()
            for moves in black_moves.values():
                all_black_moves.update(moves)
            for move in all_black_moves:
                new_black, new_white, new_board = self.adjust_positions(move, black_moves, white_moves, self.board)
                value = max(alpha, self.minimax(new_black, new_white, new_board, depth-1, alpha, beta, white))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        elif player == white:
            value = math.inf
            all_white_moves = set()
            for moves in white_moves.values():
                all_white_moves.update(moves)
            for move in all_white_moves:
                new_black, new_white, new_board = self.adjust_positions(move, black_moves, white_moves, self.board)
                value = min(value, self.minimax(new_black, new_white, new_board, depth-1, alpha, beta, black))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value
    
    def best_move(self, depth, player):
        best_moves = []
        if player == black:
            value = -math.inf
            all_black_moves = set()
            for moves in self.black_moves.values():
                all_black_moves.update(moves)
            for move in all_black_moves:
                new_black, new_white, new_board = self.adjust_positions(move, self.black_moves, self.white_moves, self.board)
                new_value = max(value, self.minimax(new_black, new_white, new_board, depth, -math.inf, math.inf, white))
                if new_value > value:
                    best_moves = []
                    value = new_value
                    best_moves.append(move)
                elif new_value == value:
                    best_moves.append(move)
        elif player == white:
            value = math.inf
            all_white_moves = set()
            for moves in self.white_moves.values():
                all_white_moves.update(moves)
            for move in all_white_moves:
                new_black, new_white, new_board = self.adjust_positions(move, self.black_moves, self. white_moves, self.board)
                new_value = min(value, self.minimax(new_black, new_white, new_board, depth, -math.inf, math.inf, black))
                if new_value < value:
                    best_moves = []
                    value = new_value
                    best_moves.append(move)
                elif new_value == value:
                    best_moves.append(move)
        move = random.choice(best_moves)
        print(f'{player} {move} has a value of {value}')
        return move

ai = ChessAI(8, 4, test_small)
ai.play()


