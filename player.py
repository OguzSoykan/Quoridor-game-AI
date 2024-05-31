from bot_ai import bot_decision

class Player:
    def __init__(self, player_id, is_bot=False):
        self.player_id = player_id
        self.is_bot = is_bot
        self.wall_count = 10  # Initialize each player with 10 walls

    def make_move(self, game_board):
        if self.is_bot:
            decision = bot_decision(game_board, self.player_id)
            if decision[0] == 'move':
                game_board.make_move(self.player_id, decision)
            elif decision[0] == 'wall':
                x, y, orientation = decision[1]
                game_board.temp_wall = (x, y, orientation)
                if game_board.confirm_wall(self.player_id):
                    game_board.switch_turn()
            return decision
        return None

    def move_pawn(self, game_board, direction):
        if game_board.move_pawn(self.player_id, direction):
            return direction
        return None

