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
        ai = black if response == white else black
        self.print_board()


        while True:
            if self._has_won():
                break
            #print(script_move)
            possible_moves = self.possible_moves(player, self._black_pieces, self._white_pieces)
            #for index, move in enumerate(possible_moves):
            #    print(f'Move {index}: {move}')
            #response = '15'
            #while not response.isnumeric():
            #    print(script_move_error)
            #    response = input()
            player_move = random.choice(possible_moves)
            self._set_positions(player_move)
            ai_move = self.__best_move(self._black_pieces, self._white_pieces, 3, ai)
            self._set_positions(ai_move)
            self.print_board()
        
        print(f'The winner is: {self._has_won()}')

    def __minimax(self, black_pieces, white_pieces, depth, player):
        black_pieces = copy.deepcopy(black_pieces)
        white_pieces = copy.deepcopy(white_pieces)
        if depth == 0 or self.has_won(black_pieces, white_pieces):
            return self.evaluate(black_pieces, white_pieces)
        
        if player == black:
            value = -math.inf
            for move in self.possible_moves(player, black_pieces, white_pieces):
                new_black, new_white = self.make_move(move, black_pieces, white_pieces)
                value = max(value, self.__minimax(new_black, new_white, depth-1, white))
            return value
        elif player == white:
            value = math.inf
            for move in self.possible_moves(player, black_pieces, white_pieces):
                new_black, new_white = self.make_move(move, black_pieces, white_pieces)
                value = min(value, self.__minimax(new_black, new_white, depth-1, black))
            return value
    
    def __best_move(self, black_pieces, white_pieces, depth, player):
        best_moves = []
        black_pieces = copy.deepcopy(black_pieces)
        white_pieces = copy.deepcopy(white_pieces)
        if player == black:
            value = -math.inf
            for move in self.possible_moves(player, black_pieces, white_pieces):
                new_black, new_white = self.make_move(move, black_pieces, white_pieces)
                new_value = max(value, self.__minimax(new_black, new_white, depth, white))
                if new_value > value:
                    best_moves = []
                    value = new_value
                    best_moves.append(move)
                elif new_value == value:
                    best_moves.append(move)
        elif player == white:
            value = math.inf
            for move in self.possible_moves(player, black_pieces, white_pieces):
                new_black, new_white = self.make_move(move, black_pieces, white_pieces)
                new_value = min(value, self.__minimax(new_black, new_white, depth, black))
                if new_value < value:
                    best_moves = []
                    value = new_value
                    best_moves.append(move)
                elif new_value == value:
                    best_moves.append(move)
        move = random.choice(best_moves)
        print(f'Move, {move} has value of {value}')
        return move

ai = ChessAI(8, 4, test_small)
ai.play()


