from chess import ChessBoard
import math
import random

script_player = "Do you want to be the white or black player?"
script_player_error = "I'm sorry. Please enter white or black."
script_move = "Please choose a move below."
script_move_error = "Move must be an integer. For example, '2'."

class ChessAI(ChessBoard):
    def play(self):
        print(script_player)
        response = input()
        while response != 'white' and response != 'black':
            print(script_player_error)
            response = input()
        player = response
        ai = 'black' if response == 'white' else 'black'

        self.print_board(self.board)
        print(script_move)
        possible_moves = self.possible_moves(player)
        for index, move in enumerate(possible_moves):
            print(f'Move {index}: {move}')
        response = input()
        while not response.isnumeric():
            print(script_move_error)
            response = input()
        player_move = possible_moves[int(response)]
        self.make_move(player_move)
        ai_move = self.__best_move(3, player=ai)
        self.make_move(ai_move)
        self.print_board(self.board)

    def __minimax(self, board, depth=3, player='white'):
        if depth == 0 or self.has_won(board):
            return self.evaluate(board)
        
        if player == 'white':
            value = -math.inf
            for move in self.possible_moves(board):
                new_board = self.make_move(move)
                value = max(value, self.__minimax(new_board, depth - 1, 'black'))
            return value
        else:
            value = math.inf
            for move in self.possible_moves(board):
                new_board = self.make_move(move)
                value = min(value, self.__minimax(new_board, depth -1, 'white'))
            return value
    
    def __best_move(self, depth, player):
        best_moves = []
        if player == 'white':
            value = -math.inf
            for move in self.possible_moves(self.board):
                new_board = self.make_move(move)
                new_value = max(value, self.__minimax(new_board, depth, 'black'))
                if new_value > value:
                    best_moves = []
                    value = new_value
                    best_moves.append(move)
                elif new_value == value:
                    best_moves.append(move)
        else:
            print('here????')
            value = math.inf
            for move in self.possible_moves(self.board):
                new_board = self.make_move(move)
                new_value = min(value, self.__minimax(new_board, depth -1, 'white')) 
                if new_value < value:
                    best_moves = []
                    value = new_value
                    best_moves.append(move)
                elif new_value == value:
                    best_moves.append(move)
        
        print(best_moves)
        return random.choice(best_moves)

ai = ChessAI()
ai.play()


