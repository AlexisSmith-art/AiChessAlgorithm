from chess import ChessBoard
import math
import random
import time
from datetime import datetime

black = 'black'
white = 'white'
script_player = "Do you want to be the white or black player?\n"
script_player_error = "I'm sorry. Please enter white or black.\n"
script_move = "Please choose a move below.\n"
script_move_error = "Move must be an integer. For example, '2'.\n"

move_set = 'moves'
priority = 'priority'

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
        response = input(script_player)
        while response != white and response != black:
            response = input(script_player_error)
        player = response
        ai = black if response == white else white
        print(f'player is: {player}, ai is: {ai}')

        counter = 0
        all_time = []
        depth = 3
        while True:
            counter += 1
            if player == black:
                possible_moves = self.get_prioritized_moves(black)
            elif player == white:
                possible_moves = self.get_prioritized_moves(white)
            #print(script_move)
            #for index, move in enumerate(possible_moves):
            #    print(f'Move {index}: {move}')
            #response = '15'
            #while not response.isnumeric():
            #    print(script_move_error)
            #    response = input()
            player_move = random.choice(possible_moves)

            self.print_board()
            self._adjust_positions(player_move)
            value = self.evaluate(self.board)
            print(f'{player} {player_move} has a value of {value}')

            if self.has_won(self.black_moves, self.white_moves):
                break
            
            before = time.perf_counter()
            self.print_board()
            ai_move = self.best_move(depth, ai)
            self._adjust_positions(ai_move)
            value = self.evaluate(self.board)
            print(f'{ai} {ai_move} has a value of {value}')
            after = time.perf_counter()
            total_time = after - before
            all_time.append(total_time)
            print(f'Took {total_time} seconds')

            if self.has_won(self.black_moves, self.white_moves):
                break
        
        self.print_board()
        win_text = f'The winner is: {self.has_won(self.black_moves, self.white_moves)} in {counter} moves'
        time_text = f'The ai({ai}) took an average of {sum(all_time)/len(all_time)}s per turn to make a move with a depth of {depth}.'
        self.log_AI(win_text, time_text)
        print(win_text)
        print(time_text)

    # Returns the best move give a player and a minimax depth.
    def best_move(self, depth, player):
        best_moves = []
        if player == black:
            value = -math.inf
            all_black_moves = self.get_prioritized_moves(black)
            for move in all_black_moves:
                new_black, new_white, new_board = self.adjust_positions(move, self.black_moves, self.white_moves, self.board)
                new_value = max(value, self.minimax(new_black, new_white, new_board, depth, -math.inf, math.inf, white))
                self.set_priority(move, new_value)
                if new_value > value:
                    best_moves = []
                    value = new_value
                    best_moves.append(move)
                elif new_value == value:
                    best_moves.append(move)
        elif player == white:
            value = math.inf
            all_white_moves = self.get_prioritized_moves(white)
            for move in all_white_moves:
                new_black, new_white, new_board = self.adjust_positions(move, self.black_moves, self. white_moves, self.board)
                new_value = min(value, self.minimax(new_black, new_white, new_board, depth, -math.inf, math.inf, black))
                self.set_priority(move, new_value)
                if new_value < value:
                    best_moves = []
                    value = new_value
                    best_moves.append(move)
                elif new_value == value:
                    best_moves.append(move)
        move = random.choice(best_moves)
        return move


    # depth-limited minimax with alpha-beta pruning
    def minimax(self, black_moves, white_moves, board, depth, alpha, beta, player):
        if depth == 0 or self.has_won(black_moves, white_moves):
            return self.evaluate(board)

        if player == black:
            value = -math.inf
            all_black_moves = self.get_moves(black_moves)
            for move in all_black_moves:
                new_black, new_white, new_board = self.adjust_positions(move, black_moves, white_moves, board)
                value = max(alpha, self.minimax(new_black, new_white, new_board, depth-1, alpha, beta, white))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        elif player == white:
            value = math.inf
            all_white_moves = self.get_moves(white_moves)
            for move in all_white_moves:
                new_black, new_white, new_board = self.adjust_positions(move, black_moves, white_moves, board)
                value = min(value, self.minimax(new_black, new_white, new_board, depth-1, alpha, beta, black))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value
    
    def log_AI(self, winner, time):
        with open('AiChessAlgorithm/chess_log.txt', 'w') as f:
            f.write(
f'''-----------------------------------------------------------------

{datetime.now()}
{winner}
{time}

-----------------------------------------------------------------''')


ai = ChessAI(8, 4, test_small)
ai.play()


