import math
import random
import time

class MCTSNode:
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.children = []
        self.move = move
        self.visits = 0
        self.wins = 0

    def is_fully_expanded(self):
        all_moves = self.game_state.get_all_possible_moves(self.game_state.current_player())
        expanded_moves = [child.move for child in self.children]
        return set(all_moves) == set(expanded_moves)

    def best_child(self, c_param=1.4):
        choices_weights = [(child.wins / child.visits) + c_param * math.sqrt((2 * math.log(self.visits) / child.visits)) for child in self.children]
        return self.children[choices_weights.index(max(choices_weights))]

    def rollout_policy(self, possible_moves):
        return possible_moves[random.randint(0, len(possible_moves) - 1)]

    def expand(self):
        untried_moves = [move for move in self.game_state.get_all_possible_moves(self.game_state.current_player()) if move not in [child.move for child in self.children]]
        if not untried_moves:
            return None

        move = random.choice(untried_moves)
        next_state = self.game_state.clone()

        # Validate move before applying it
        if move[0] == 'move' and not next_state.is_move_legal(self.game_state.current_player(), move[1]):
            return None

        next_state.make_move(self.game_state.current_player(), move)
        next_state.switch_turn()
        child_node = MCTSNode(next_state, parent=self, move=move)
        self.children.append(child_node)
        return child_node

    def rollout(self):
        current_rollout_state = self.game_state.clone()
        depth = 0
        max_depth = 50  # Limit depth to prevent infinite rollouts
        while not current_rollout_state.check_winner() and depth < max_depth:
            possible_moves = current_rollout_state.get_all_possible_moves(current_rollout_state.current_player())
            if not possible_moves:
                break
            move = self.rollout_policy(possible_moves)

            # Validate move before applying it
            if move[0] == 'move' and not current_rollout_state.is_move_legal(current_rollout_state.current_player(), move[1]):
                continue

            current_rollout_state.make_move(current_rollout_state.current_player(), move)
            current_rollout_state.switch_turn()
            depth += 1
        return current_rollout_state.check_winner()

    def backpropagate(self, result):
        self.visits += 1
        if result == self.game_state.current_player():
            self.wins += 1
        if self.parent:
            self.parent.backpropagate(result)

def mcts(game_state, num_simulations, max_time=5.0):
    root = MCTSNode(game_state)
    start_time = time.time()

    for _ in range(num_simulations):
        if time.time() - start_time > max_time:
            break
        node = root
        while node.is_fully_expanded():
            node = node.best_child()
        if not node.game_state.check_winner():
            node = node.expand()
        if node:
            result = node.rollout()
            node.backpropagate(result)

    best_move = root.best_child(c_param=0.0).move
    return best_move

def evaluate_wall_placement(game_board, player_index, wall_position):
    x, y, orientation = wall_position
    opponent_index = 1 - player_index

    # Temporarily place the wall
    game_board.walls.add((x, y, orientation, player_index))
    opponent_path_length = len(game_board.get_shortest_path(opponent_index))
    # Remove the wall after evaluation
    game_board.walls.remove((x, y, orientation, player_index))

    return opponent_path_length



def bot_decision(game_board, bot_player_index):
    num_simulations = 1000
    player = game_board.players[bot_player_index]

    possible_moves = game_board.get_all_possible_moves(bot_player_index)
    valid_moves = []
    for move in possible_moves:
        if move[0] == 'move' and game_board.is_move_legal(bot_player_index, move[1]):
            valid_moves.append(move)
        elif move[0] == 'wall' and game_board.is_wall_placement_valid(*move[1]):
            valid_moves.append(move)

    print(f"Bot {bot_player_index}: Valid moves - {valid_moves}")

    # If there are walls left, evaluate the best wall placement
    if player.wall_count > 0 and any(move[0] == 'wall' for move in valid_moves):
        blocking_walls = [(move, evaluate_wall_placement(game_board, bot_player_index, move[1])) for move in valid_moves if move[0] == 'wall']
        print(f"Bot {bot_player_index}: Blocking walls - {blocking_walls}")
        if blocking_walls:
            # Extract the path length value correctly
            best_wall, best_wall_path_length = max(blocking_walls, key=lambda x: x[1])
            # Calculate the bot's own shortest path length
            bot_path_length = len(game_board.get_shortest_path(bot_player_index))
            print(f"Bot {bot_player_index}: Best wall - {best_wall}, Opponent path length - {best_wall_path_length}, Bot path length - {bot_path_length}")
            # If the best wall placement significantly increases the opponent's path, choose to place the wall
            if best_wall_path_length > bot_path_length:  # Adjust the threshold as needed
                print(f"Bot {bot_player_index}: Placing wall at {best_wall}")
                return best_wall

    # If no walls left or no beneficial wall moves, go for winning
    valid_moves = [move for move in valid_moves if move[0] == 'move']
    if valid_moves:
        goal_row = 8 if bot_player_index == 0 else 0
        valid_moves.sort(key=lambda move: game_board.get_shortest_path_length(bot_player_index, move[1]))
        best_move = valid_moves[0]
    else:
        best_move = ('move', 'down')  # Fallback move

    print(f"Bot {bot_player_index}: Moving to {best_move}")
    return best_move






