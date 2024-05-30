class GameBoard:
    def __init__(self):
        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.pawns = [(4, 0), (4, 8)]  # Starting positions for 2-player game
        self.walls = set()
        self.temp_wall = None  # Temporary wall position and orientation (x, y, orientation)

    def toggle_temp_wall(self, x, y):
        if self.temp_wall and self.temp_wall[:2] == (x, y):
            new_orientation = 'v' if self.temp_wall[2] == 'h' else 'h'
            self.temp_wall = (x, y, new_orientation)
            print(f"Toggled to {new_orientation} wall at ({x}, {y})")
        else:
            self.temp_wall = (x, y, 'h')
            print(f"Placed horizontal temporary wall at ({x}, {y})")

    def confirm_wall(self, player_index):
        if not self.temp_wall:
            return False
        
        x, y, orientation = self.temp_wall
        if self.is_wall_placement_valid(x, y, orientation):
            self.walls.add((x, y, orientation, player_index))
            self.temp_wall = None
            return True
        return False

    def is_wall_placement_valid(self, x, y, orientation):
        # Example: Ensure walls don't overlap and don't block all paths
        for wx, wy, worientation, _ in self.walls:
            if (x, y) == (wx, wy) and orientation == worientation:
                return False
        return True

    def is_move_legal(self, pawn_index, direction):
        # Simplified example logic for move legality
        x, y = self.pawns[pawn_index]
        if direction == 'up' and y > 0:
            return True
        if direction == 'down' and y < 8:
            return True
        if direction == 'left' and x > 0:
            return True
        if direction == 'right' and x < 8:
            return True
        return False

    def move_pawn(self, pawn_index, direction):
        # Example logic for moving the pawn
        x, y = self.pawns[pawn_index]
        if direction == 'up' and y > 0:
            self.pawns[pawn_index] = (x, y - 1)
            return True
        if direction == 'down' and y < 8:
            self.pawns[pawn_index] = (x, y + 1)
            return True
        if direction == 'left' and x > 0:
            self.pawns[pawn_index] = (x - 1, y)
            return True
        if direction == 'right' and x < 8:
            self.pawns[pawn_index] = (x + 1, y)
            return True
        return False

    def check_winner(self):
        for idx, (x, y) in enumerate(self.pawns):
            if idx == 0 and y == 8:
                return 0
            if idx == 1 and y == 0:
                return 1
        return None
