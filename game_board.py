from collections import deque
from player import Player

class GameBoard:
    def __init__(self, player_types):
        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.pawns = [(4, 0), (4, 8)]  # Starting positions for 2-player game
        self.walls = set()
        self.temp_wall = None  # Temporary wall position and orientation (x, y, orientation)
        self.players = [Player(0, is_bot=(player_types[0] == 1)), Player(1, is_bot=(player_types[1] == 1))]  # Initialize players with types
        self.current_player_index = 0

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
            player.wall_count -= 1  # Ensure wall count is decremented here
            return True
        return False

    def bfs(self, start, goal_row):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Down, up, right, left
        queue = deque([start])
        visited = set([start])

        while queue:
            x, y = queue.popleft()
            if y == goal_row:
                return True
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 9 and 0 <= ny < 9 and (nx, ny) not in visited:
                    if not self.is_wall_blocking(x, y, 'down' if dy == 1 else 'up' if dy == -1 else 'right' if dx == 1 else 'left'):
                        queue.append((nx, ny))
                        visited.add((nx, ny))
        return False

    def is_wall_placement_valid(self, x, y, orientation):
        if orientation == 'h':
            if x < 0 or x >= 8 or y < 0 or y >= 8:
                return False
        elif orientation == 'v':
            if x < 0 or x >= 8 or y < 0 or y >= 8:
                return False

        original_walls = self.walls.copy()
        self.walls.add((x, y, orientation, -1))

        for wx, wy, worientation, _ in original_walls:
            if orientation == 'h':
                if worientation == 'h' and ((wx == x and wy == y) or (wx == x + 1 and wy == y) or (wx == x - 1 and wy == y)):
                    self.walls = original_walls
                    return False
                if worientation == 'v' and (wx == x and wy == y):
                    self.walls = original_walls
                    return False
            if orientation == 'v':
                if worientation == 'v' and ((wx == x and wy == y) or (wx == x and wy == y + 1) or (wx == x and wy == y - 1)):
                    self.walls = original_walls
                    return False
                if worientation == 'h' and (wx == x and wy == y):
                    self.walls = original_walls
                    return False

        valid_paths = all(self.bfs((px, py), 8 if idx == 0 else 0) for idx, (px, py) in enumerate(self.pawns))
        self.walls = original_walls

        return valid_paths

    def is_wall_blocking(self, x, y, direction):
        def wall_exists(check_x, check_y, orientation):
            return any(wall[:3] == (check_x, check_y, orientation) for wall in self.walls)

        if direction == 'up':
            if wall_exists(x, y - 1, 'h') or wall_exists(x - 1, y - 1, 'h'):
                return True
        elif direction == 'down':
            if wall_exists(x, y, 'h') or wall_exists(x - 1, y, 'h'):
                return True
        elif direction == 'left':
            if wall_exists(x - 1, y, 'v') or wall_exists(x - 1, y - 1, 'v'):
                return True
        elif direction == 'right':
            if wall_exists(x, y, 'v') or wall_exists(x, y - 1, 'v'):
                return True
        return False

    def is_move_legal(self, pawn_index, direction):
        x, y = self.pawns[pawn_index]
        opponent_index = 1 - pawn_index
        opponent_x, opponent_y = self.pawns[opponent_index]

        if direction == 'up':
            if y > 0 and not self.is_wall_blocking(x, y, 'up'):
                if (x, y - 1) == (opponent_x, opponent_y):
                    # Check if jump is possible
                    if y > 1 and not self.is_wall_blocking(x, y - 1, 'up') and not self.is_position_occupied(x, y - 2):
                        return True
                else:
                    return not self.is_position_occupied(x, y - 1)
        elif direction == 'down':
            if y < 8 and not self.is_wall_blocking(x, y, 'down'):
                if (x, y + 1) == (opponent_x, opponent_y):
                    # Check if jump is possible
                    if y < 7 and not self.is_wall_blocking(x, y + 1, 'down') and not self.is_position_occupied(x, y + 2):
                        return True
                else:
                    return not self.is_position_occupied(x, y + 1)
        elif direction == 'left':
            if x > 0 and not self.is_wall_blocking(x, y, 'left'):
                if (x - 1, y) == (opponent_x, opponent_y):
                    # Check if jump is possible
                    if x > 1 and not self.is_wall_blocking(x - 1, y, 'left') and not self.is_position_occupied(x - 2, y):
                        return True
                else:
                    return not self.is_position_occupied(x - 1, y)
        elif direction == 'right':
            if x < 8 and not self.is_wall_blocking(x, y, 'right'):
                if (x + 1, y) == (opponent_x, opponent_y):
                    # Check if jump is possible
                    if x < 7 and not self.is_wall_blocking(x + 1, y, 'right') and not self.is_position_occupied(x + 2, y):
                        return True
                else:
                    return not self.is_position_occupied(x + 1, y)

        return False



    def make_move(self, player_id, move):
        print(f"Player {player_id} making move: {move}")
        if move[0] == 'move':
            direction = move[1]
            if not self.is_move_legal(player_id, direction):
                print(f"Illegal move attempted by player {player_id}: {move}")
                return False
            success = self.move_pawn(player_id, direction)
            if success:
                self.switch_turn()
            print(f"Move result for player {player_id}: {success}")
            return success
        elif move[0] == 'wall':
            position = move[1]
            success = self.place_wall(player_id, position)
            if success:
                self.switch_turn()
            print(f"Wall placement result for player {player_id}: {success}")
            return success
        else:
            print("Invalid move type")
            return False



    def is_position_occupied(self, x, y):
        return any(px == x and py == y for px, py in self.pawns)

    def move_pawn(self, pawn_index, direction):
        if not self.is_move_legal(pawn_index, direction):
            print(f"Move {direction} for pawn {pawn_index} is illegal")
            return False

        x, y = self.pawns[pawn_index]
        opponent_index = 1 - pawn_index
        opponent_x, opponent_y = self.pawns[opponent_index]

        if direction == 'up':
            if (x, y - 1) == (opponent_x, opponent_y) and y > 1 and not self.is_wall_blocking(x, y - 1, 'up'):
                self.pawns[pawn_index] = (x, y - 2)
            else:
                self.pawns[pawn_index] = (x, y - 1)
        elif direction == 'down':
            if (x, y + 1) == (opponent_x, opponent_y) and y < 7 and not self.is_wall_blocking(x, y + 1, 'down'):
                self.pawns[pawn_index] = (x, y + 2)
            else:
                self.pawns[pawn_index] = (x, y + 1)
        elif direction == 'left':
            if (x - 1, y) == (opponent_x, opponent_y) and x > 1 and not self.is_wall_blocking(x - 1, y, 'left'):
                self.pawns[pawn_index] = (x - 2, y)
            else:
                self.pawns[pawn_index] = (x - 1, y)
        elif direction == 'right':
            if (x + 1, y) == (opponent_x, opponent_y) and x < 7 and not self.is_wall_blocking(x + 1, y, 'right'):
                self.pawns[pawn_index] = (x + 2, y)
            else:
                self.pawns[pawn_index] = (x + 1, y)
        else:
            return False

        return True

        if new_position:
            new_x, new_y = new_position
            # Ensure the move is only one square
            if abs(new_x - x) > 1 or abs(new_y - y) > 1:
                print(f"Illegal move detected: {direction}, from ({x}, {y}) to ({new_x}, {new_y})")
                return False
            self.pawns[pawn_index] = new_position
            print(f"After moving pawn {pawn_index}: {self.pawns}")
            return True

        print(f"Illegal move attempt: {direction}")
        return False


    def place_wall(self, player_index, wall_detail):
        x, y, orientation = wall_detail
        if self.is_wall_placement_valid(x, y, orientation):
            self.walls.add((x, y, orientation, player_index))
            self.players[player_index].wall_count -= 1
            return True
        return False

    def get_all_possible_moves(self, player_index):
        moves = []
        directions = ['up', 'down', 'left', 'right']

        for direction in directions:
            if self.is_move_legal(player_index, direction):
                moves.append(('move', direction))

        for x in range(8):
            for y in range(8):
                for orientation in ['h', 'v']:
                    if self.is_wall_placement_valid(x, y, orientation):
                        moves.append(('wall', (x, y, orientation)))

        return moves


    def get_valid_pawn_moves(self, player_index):
        valid_moves = []
        directions = ['up', 'down', 'left', 'right']
        for direction in directions:
            if self.is_move_legal(player_index, direction):
                valid_moves.append(direction)
        return valid_moves

    def get_valid_wall_placements(self, player_index):
        valid_walls = []
        for x in range(8):
            for y in range(8):
                for orientation in ['h', 'v']:
                    if self.is_wall_placement_valid(x, y, orientation):
                        valid_walls.append((x, y, orientation))
        return valid_walls

    def undo_move(self, player_index, move):
        move_type, move_detail = move
        if move_type == 'pawn':
            x, y = self.pawns[player_index]
            if move_detail == 'up':
                self.pawns[player_index] = (x, y + 1)
            elif move_detail == 'down':
                self.pawns[player_index] = (x, y - 1)
            elif move_detail == 'left':
                self.pawns[player_index] = (x + 1, y)
            elif move_detail == 'right':
                self.pawns[player_index] = (x - 1, y)
        elif move_type == 'wall':
            x, y, orientation = move_detail
            self.walls.remove((x, y, orientation, player_index))
            self.players[player_index].wall_count += 1

    def check_winner(self):
        for idx, (x, y) in enumerate(self.pawns):
            if idx == 0 and y == 8:
                return 0
            if idx == 1 and y == 0:
                return 1
        return None


    def current_player(self):
        return self.current_player_index

    def switch_turn(self):
        self.current_player_index = 1 - self.current_player_index

    def clone(self):
        clone_board = GameBoard([player.is_bot for player in self.players])
        clone_board.pawns = self.pawns[:]
        clone_board.walls = self.walls.copy()
        clone_board.temp_wall = self.temp_wall
        clone_board.current_player_index = self.current_player_index
        return clone_board
