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
            print(f"Invalid move {move} during expansion")
            return None

        next_state.make_move(self.game_state.current_player(), move)
        next_state.switch_turn()
        child_node = MCTSNode(next_state, parent=self, move=move)
        self.children.append(child_node)
        print(f"Expanded node with move: {move}")
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
        print(f"Rollout result: {current_rollout_state.check_winner()}, depth: {depth}")
        return current_rollout_state.check_winner()

    def backpropagate(self, result):
        self.visits += 1
        if result == self.game_state.current_player():
            self.wins += 1
        if self.parent:
            self.parent.backpropagate(result)
        print(f"Backpropagating result: {result}, current node visits: {self.visits}, wins: {self.wins}")

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
    print(f"Best move determined by MCTS: {best_move}")
    return best_move

def bot_decision(game_board, bot_player_index):
    num_simulations = 1000
    player = game_board.players[bot_player_index]

    possible_moves = game_board.get_all_possible_moves(bot_player_index)
    print(f"Possible moves for bot: {possible_moves}")  # Debugging information

    valid_moves = []
    for move in possible_moves:
        if move[0] == 'move' and game_board.is_move_legal(bot_player_index, move[1]):
            valid_moves.append(move)
        elif move[0] == 'wall' and game_board.is_wall_placement_valid(*move[1]):
            valid_moves.append(move)

    print(f"Valid moves for bot: {valid_moves}")  # Debugging information

    if player.wall_count > 0 and 'wall' in (move[0] for move in valid_moves):
        best_move = mcts(game_board, num_simulations)
    else:
        valid_moves = [move for move in valid_moves if move[0] == 'move']
        if valid_moves:
            best_move = random.choice(valid_moves)
        else:
            best_move = ('move', 'down')  # Fallback move

    print(f"Bot decision: {best_move}")  # Debugging information
    return best_move










