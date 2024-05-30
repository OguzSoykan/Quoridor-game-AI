# player.py

class Player:
    def __init__(self, player_id, is_bot=False):
        self.player_id = player_id
        self.is_bot = is_bot
        self.wall_count = 10  # Initialize each player with 10 walls

    def make_move(self, game_board):
        if self.is_bot:
            return self.calculate_bot_move(game_board)
        return None

    def calculate_bot_move(self, game_board):
        # Implement AI logic here or call bot_ai.py functions
        pass
