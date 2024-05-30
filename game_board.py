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
            self.temp_wall = None
            player.wall_count -= 1
            return True
        return False

    def is_wall_placement_valid(self, x, y, orientation):
        # Ensure the wall is within the grid boundaries
        if orientation == 'h':
            if x < 0 or x >= 8 or y < 0 or y >= 8:  # x range is 0-7 because horizontal walls span across cells
                return False
        elif orientation == 'v':
            if x < 0 or x >= 8 or y < 0 or y >= 8:  # y range is 0-7 because vertical walls span across cells
                return False

        # Check for overlap with existing walls
        for wx, wy, worientation, _ in self.walls:
            if orientation == 'h':
                if worientation == 'h' and ((wx == x and wy == y) or (wx == x + 1 and wy == y) or (wx == x - 1 and wy == y)):
                    return False
                if worientation == 'v' and (wx == x and wy == y):
                    return False
            if orientation == 'v':
                if worientation == 'v' and ((wx == x and wy == y) or (wx == x and wy == y + 1) or (wx == x and wy == y - 1)):
                    return False
                if worientation == 'h' and (wx == x and wy == y):
                    return False

        return True    
    
    def is_wall_blocking(self, x, y, direction):
        print(f"Checking wall blocking for direction {direction} at ({x}, {y})")
        print(f"Current walls: {self.walls}")

        def wall_exists(check_x, check_y, orientation):
            exists = any(wall[:3] == (check_x, check_y, orientation) for wall in self.walls)
            print(f"Checking wall existence at ({check_x}, {check_y}, {orientation}): {exists}")
            return exists

        if direction == 'up':
            if wall_exists(x, y - 1, 'h') or wall_exists(x - 1, y - 1, 'h'):
                print(f"Wall blocking move up at ({x}, {y-1}) or ({x - 1}, {y - 1})")
                return True
        elif direction == 'down':
            if wall_exists(x, y, 'h') or wall_exists(x - 1, y, 'h'):
                print(f"Wall blocking move down at ({x}, {y}) or ({x - 1}, {y})")
                return True
        elif direction == 'left':
            if wall_exists(x - 1, y, 'v') or wall_exists(x - 1, y - 1, 'v'):
                print(f"Wall blocking move left at ({x - 1}, {y}) or ({x - 1}, {y - 1})")
                return True
        elif direction == 'right':
            if wall_exists(x, y, 'v') or wall_exists(x, y - 1, 'v'):
                print(f"Wall blocking move right at ({x}, {y}) or ({x}, {y - 1})")
                return True
        print(f"No wall blocking for direction {direction} at ({x}, {y})")
        return False
       
    def is_move_legal(self, pawn_index, direction):
        x, y = self.pawns[pawn_index]
        print(f"Checking move for pawn {pawn_index} at ({x}, {y}) in direction {direction}")

        if direction == 'up':
            if y > 0:
                if self.is_position_occupied(x, y - 1):
                    if y > 1 and not self.is_position_occupied(x, y - 2) and not self.is_wall_blocking(x, y - 1, 'up') and not self.is_wall_blocking(x, y, 'up'):
                        return True
                elif not self.is_wall_blocking(x, y, direction):
                    return True

        elif direction == 'down':
            if y < 8:
                if self.is_position_occupied(x, y + 1):
                    if y < 7 and not self.is_position_occupied(x, y + 2) and not self.is_wall_blocking(x, y + 1, 'down') and not self.is_wall_blocking(x, y, 'down'):
                        return True
                elif not self.is_wall_blocking(x, y, direction):
                    return True

        elif direction == 'left':
            if x > 0:
                if self.is_position_occupied(x - 1, y):
                    if x > 1 and not self.is_position_occupied(x - 2, y) and not self.is_wall_blocking(x - 1, y, 'left') and not self.is_wall_blocking(x, y, 'left'):
                        return True
                elif not self.is_wall_blocking(x, y, direction):
                    return True

        elif direction == 'right':
            if x < 8:
                if self.is_position_occupied(x + 1, y):
                    if x < 7 and not self.is_position_occupied(x + 2, y) and not self.is_wall_blocking(x + 1, y, 'right') and not self.is_wall_blocking(x, y, 'right'):
                        return True
                elif not self.is_wall_blocking(x, y, direction):
                    return True

        return False

    def is_position_occupied(self, x, y):
        return any(px == x and py == y for px, py in self.pawns)

    def move_pawn(self, pawn_index, direction):
        if not self.is_move_legal(pawn_index, direction):
            return False

        x, y = self.pawns[pawn_index]
        if direction == 'up':
            if self.is_position_occupied(x, y - 1):
                self.pawns[pawn_index] = (x, y - 2)
            else:
                self.pawns[pawn_index] = (x, y - 1)
        elif direction == 'down':
            if self.is_position_occupied(x, y + 1):
                self.pawns[pawn_index] = (x, y + 2)
            else:
                self.pawns[pawn_index] = (x, y + 1)
        elif direction == 'left':
            if self.is_position_occupied(x - 1, y):
                self.pawns[pawn_index] = (x - 2, y)
            else:
                self.pawns[pawn_index] = (x - 1, y)
        elif direction == 'right':
            if self.is_position_occupied(x + 1, y):
                self.pawns[pawn_index] = (x + 2, y)
            else:
                self.pawns[pawn_index] = (x + 1, y)
        return True

    def check_winner(self):
        for idx, (x, y) in enumerate(self.pawns):
            if idx == 0 and y == 8:
                return 0
            if idx == 1 and y == 0:
                return 1
        return None
