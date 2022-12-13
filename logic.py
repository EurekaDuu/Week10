# This file is where game logic lives. No input
# or output happens here. The logic in this file
# should be unit-testable.
import random

class Player:
    x_move = 0
    y_move = 0
    def __init__(self, name):
        self.name = name

class Game:
    board = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]

    def reset(self):
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    def update_board(self, x, y, player_name):
        self.board[x][y] = player_name

    def get_winner(self):
        """Determines the winner of the given board.
        Returns 'X', 'O', or None."""
        player_x_moves=[0]*8
        player_o_moves=[0]*8
        action_count = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "X":
                    player_x_moves[i] += 1
                    player_x_moves[j+3] += 1
                    if i == j:
                        player_x_moves[6] += 1
                    if i == 2 - j:
                        player_x_moves[7] += 1
                    action_count += 1
                if self.board[i][j] == "O":
                    player_o_moves[i] += 1
                    player_o_moves[j+3] += 1
                    if i == j:
                        player_o_moves[6] += 1
                    if i == 2 - j:
                        player_o_moves[7] += 1
                    action_count += 1
        for i in range(8):
            if player_x_moves[i] == 3:
                return "X"
            if player_o_moves[i] == 3:
                return "O"

        if action_count == 9:
            return "Draw"
        return None


    def other_player(self, player):
        """Given the character for a player, returns the other player."""
        if player == "X":
            return "O"

        return "X"

    def get_bot_input(self):
        coordinate_set = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == None:
                    coordinate_set.append([i, j])
        random_coor = random.choice(coordinate_set)
        return random_coor[0], random_coor[1]
