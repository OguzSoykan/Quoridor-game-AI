class GameBoard:
    def __init__(self):
        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.pawns = [(4, 0), (4, 8)]  # Starting positions for 2-player game
        self.walls = set()

    def is_move_legal(self, pawn_index, direction):
        x, y = self.pawns[pawn_index]
        if direction == 'up':
            new_position = (x, y-1)
        elif direction == 'down':
            new_position = (x, y+1)
        elif direction == 'left':
            new_position = (x-1, y)
        elif direction == 'right':
            new_position = (x+1, y)
        else:
            return False

        # Check boundaries
        if not (0 <= new_position[0] < 9 and 0 <= new_position[1] < 9):
            return False

        # Check walls and other pawns
        if new_position in self.walls or new_position in self.pawns:
            return False

        if self.can_jump_over(pawn_index, direction):
            return True

        return True

    def move_pawn(self, pawn_index, direction):
        if self.is_move_legal(pawn_index, direction):
            x, y = self.pawns[pawn_index]
            if direction == 'up':
                self.pawns[pawn_index] = (x, y-1)
            elif direction == 'down':
                self.pawns[pawn_index] = (x, y+1)
            elif direction == 'left':
                self.pawns[pawn_index] = (x-1, y)
            elif direction == 'right':
                self.pawns[pawn_index] = (x+1, y)
            return True
        return False

    def can_place_wall(self, position, orientation):
        x, y = position
        if orientation == 'h':
            if y == 0 or y >= 8 or (x, y - 1, 'h') in self.walls or (x, y, 'h') in self.walls:
                return False
        elif orientation == 'v':
            if x == 0 or x >= 8 or (x - 1, y, 'v') in self.walls or (x, y, 'v') in self.walls:
                return False
        return True

    def place_wall(self, position, orientation, player_index):
        x, y = position
        if self.can_place_wall(position, orientation):
            self.walls.add((x, y, orientation, player_index))  # Store player index with wall
            return True
        return False

    def can_jump_over(self, pawn_index, direction):
        x, y = self.pawns[pawn_index]
        if direction == 'up' and y > 1:
            if (x, y - 1) in self.pawns and (x, y - 2) not in self.pawns:
                return True
        return False

    def check_winner(self):
        for index, (x, y) in enumerate(self.pawns):
            if (index == 0 and y == 8) or (index == 1 and y == 0):
                return index + 1  # Return 1 or 2 to indicate the winner
        return None
