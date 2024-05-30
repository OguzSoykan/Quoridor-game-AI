# game_board.py

from player import Player

class GameBoard:
    def __init__(self):
        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.pawns = [(4, 0), (4, 8)]  # Starting positions for 2-player game
        self.walls = set()
        self.temp_wall = None  # Temporary wall position and orientation (x, y, orientation)
        self.players = [Player(0), Player(1)]  # Initialize players

    def toggle_temp_wall(self, x, y):
        if self.temp_wall and self.temp_wall[:2] == (x, y):
            new_orientation = 'v' if self.temp_wall[2] == 'h' else 'h'
            self.temp_wall = (x, y, new_orientation)
        else:
            self.temp_wall = (x, y, 'h')

    def confirm_wall(self, player_index):
        if not self.temp_wall:
            return False
        
        player = self.players[player_index]
        if player.wall_count <= 0:
            return False
        
        x, y, orientation = self.temp_wall
        if self.is_wall_placement_valid(x, y, orientation):
            self.walls.add((x, y, orientation, player_index))
            print(f"Wall added at: {(x, y, orientation)}")
            self.temp_wall = None
            player.wall_count -= 1  # Decrease the wall count
            return True
        return False

    def is_wall_placement_valid(self, x, y, orientation):
        # Ensure walls don't overlap and don't block all paths
        for wx, wy, worientation, _ in self.walls:
            if (x, y) == (wx, wy) and orientation == worientation:
                return False
        return True



    def is_wall_blocking(self, x, y, direction):
        print(f"Checking wall blocking for direction {direction} at ({x}, {y})")
        print(f"Current walls: {self.walls}")
        
        def wall_exists(check_x, check_y, orientation):
            return any(wall[:3] == (check_x, check_y, orientation) for wall in self.walls)
        
        if direction == 'up':
            if wall_exists(x, y - 1, 'h') or wall_exists(x - 1, y - 1, 'h') or wall_exists(x, y, 'h'):
                print(f"Wall blocking move up at ({x}, {y-1}) or ({x - 1, y - 1}) or ({x, y})")
                return True
        elif direction == 'down':
            if wall_exists(x, y, 'h') or wall_exists(x - 1, y, 'h') or wall_exists(x, y + 1, 'h'):
                print(f"Wall blocking move down at ({x}, {y}) or ({x - 1, y}) or ({x, y + 1})")
                return True
        elif direction == 'left':
            if wall_exists(x - 1, y, 'v') or wall_exists(x - 1, y - 1, 'v') or wall_exists(x, y, 'v'):
                print(f"Wall blocking move left at ({x - 1, y}) or ({x - 1, y - 1}) or ({x, y})")
                return True
        elif direction == 'right':
            if wall_exists(x, y, 'v') or wall_exists(x, y - 1, 'v') or wall_exists(x + 1, y, 'v'):
                print(f"Wall blocking move right at ({x, y}) or ({x, y - 1}) or ({x + 1, y})")
                return True
        print(f"No wall blocking for direction {direction} at ({x}, {y})")
        return False

    def is_move_legal(self, pawn_index, direction):
        x, y = self.pawns[pawn_index]
        print(f"Checking move for pawn {pawn_index} at ({x}, {y}) in direction {direction}")
        
        if direction == 'up' and y > 0 and not self.is_wall_blocking(x, y, direction):
            print(f"Move up is legal for pawn {pawn_index} at ({x}, {y})")
            return True
        if direction == 'down' and y < 8 and not self.is_wall_blocking(x, y, direction):
            print(f"Move down is legal for pawn {pawn_index} at ({x}, {y})")
            return True
        if direction == 'left' and x > 0 and not self.is_wall_blocking(x, y, direction):
            print(f"Move left is legal for pawn {pawn_index} at ({x}, {y})")
            return True
        if direction == 'right' and x < 8 and not self.is_wall_blocking(x, y, direction):
            print(f"Move right is legal for pawn {pawn_index} at ({x}, {y})")
            return True
        
        print(f"Move {direction} is not legal for pawn {pawn_index} at ({x}, {y})")
        return False

    def move_pawn(self, pawn_index, direction):
        if not self.is_move_legal(pawn_index, direction):
            return False

        x, y = self.pawns[pawn_index]
        if direction == 'up':
            self.pawns[pawn_index] = (x, y - 1)
        elif direction == 'down':
            self.pawns[pawn_index] = (x, y + 1)
        elif direction == 'left':
            self.pawns[pawn_index] = (x - 1, y)
        elif direction == 'right':
            self.pawns[pawn_index] = (x + 1, y)
        return True

    def check_winner(self):
        for idx, (x, y) in enumerate(self.pawns):
            if idx == 0 and y == 8:
                return 0
            if idx == 1 and y == 0:
                return 1
        return None
