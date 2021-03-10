from chess import ChessBoard
import math
import random
import copy

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

        current_board = self.board
        self.print_board(current_board)
        print(script_move)
        possible_moves = self.possible_moves(player, current_board)
        for index, move in enumerate(possible_moves):
            print(f'Move {index}: {move}')
        response = input()
        while not response.isnumeric():
            print(script_move_error)
            response = input()
        player_move = possible_moves[int(response)]
        current_board = self.make_move(player_move, current_board)
        self.print_board(current_board)
        ai_move = self.__best_move(current_board, 3, color=ai)
        current_board = self.make_move(ai_move, current_board)
        self.print_board(current_board)

    def __minimax(self, board, depth=3, color='white'):
        print('depth', depth)
        if depth == 0 or self.has_won(board):
            return self.evaluate(board)
        
        if color == 'white':
            value = -math.inf
            print(self.possible_moves('white', board))
            for move in self.possible_moves('white', board):
                self.print_board(board)
                print('move', move)
                new_board = self.make_move(move, board)
                value = max(value, self.__minimax(copy.deepcopy(new_board), depth-1, 'black'))
            return value
        else:
            value = math.inf
            print(self.possible_moves('black', board))
            for move in self.possible_moves('black', board):
                self.print_board(board)
                print('move', move)
                new_board = self.make_move(move, board)
                value = min(value, self.__minimax(copy.deepcopy(new_board), depth-1, 'white'))
            return value
    
    def __best_move(self, board, depth, color):
        best_moves = []
        if color == 'white':
            value = -math.inf
            for move in self.possible_moves('white', board):
                new_board = self.make_move(move, board)
                new_value = max(value, self.__minimax(copy.deepcopy(new_board), depth, 'black'))
                if new_value > value:
                    best_moves = []
                    value = new_value
                    best_moves.append(move)
                elif new_value == value:
                    best_moves.append(move)
        else:
            value = math.inf
            for move in self.possible_moves('black', board):
                new_board = self.make_move(move, board)
                new_value = min(value, self.__minimax(copy.deepcopy(new_board), depth, 'white')) 
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


