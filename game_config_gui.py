import tkinter as tk
from game_board import GameBoard

def toggle_wall_mode(wall_mode_var, button=None):
    wall_mode_var.set(not wall_mode_var.get())
    if button:
        button.config(text="Wall Mode: " + ("On" if wall_mode_var.get() else "Off"))
    print("Wall Mode: " + ("On" if wall_mode_var.get() else "Off"))

def update_player_options(num_pawns_var, player_checkbuttons):
    num_pawns = int(num_pawns_var.get())
    for i in range(4):
        player_checkbuttons[i].config(state='normal' if i < num_pawns else 'disabled')

def draw_board(canvas, game_board, selected_pawn=None):
    canvas.delete("all")
    # Draw tiles
    for i in range(9):
        for j in range(9):
            canvas.create_rectangle(i * 40, j * 40, (i + 1) * 40, (j + 1) * 40, outline="black", fill="white")

    # Draw pawns
    for idx, (x, y) in enumerate(game_board.pawns):
        fill_color = "black" if idx == 0 else "red"
        canvas.create_oval(x * 40 + 10, y * 40 + 10, x * 40 + 30, y * 40 + 30, fill=fill_color)

    # Highlight potential moves for the selected pawn
    if selected_pawn is not None:
        x, y = game_board.pawns[selected_pawn]
        for direction in ['up', 'down', 'left', 'right']:
            if game_board.is_move_legal(selected_pawn, direction):
                if direction == 'up':
                    canvas.create_rectangle(x * 40 + 10, (y - 1) * 40 + 10, x * 40 + 30, y * 40 - 10, outline="blue", fill="blue")
                elif direction == 'down':
                    canvas.create_rectangle(x * 40 + 10, (y + 1) * 40 + 10, x * 40 + 30, (y + 1) * 40 + 30, outline="blue", fill="blue")
                elif direction == 'left':
                    canvas.create_rectangle((x - 1) * 40 + 10, y * 40 + 10, x * 40 - 10, y * 40 + 30, outline="blue", fill="blue")
                elif direction == 'right':
                    canvas.create_rectangle((x + 1) * 40 + 10, y * 40 + 10, (x + 1) * 40 + 30, y * 40 + 30, outline="blue", fill="blue")

    # Draw walls
    for (wx, wy, orientation, player_index) in game_board.walls:
        color = "red" if player_index == 0 else "blue"
        if orientation == 'h':
            canvas.create_line(wx * 80 + 40, wy * 80 + 40, wx * 80 + 120, wy * 80 + 40, fill=color, width=4)
        elif orientation == 'v':
            canvas.create_line(wx * 80 + 40, wy * 80 + 40, wx * 80 + 40, wy * 80 + 120, fill=color, width=4)

def determine_direction(x, y, current_x, current_y):
    if x == current_x and y == current_y - 1:
        return 'up'
    elif x == current_x and y == current_y + 1:
        return 'down'
    elif y == current_y and x == current_x - 1:
        return 'left'
    elif y == current_y and x == current_x + 1:
        return 'right'
    return None

def on_board_click(event, canvas, game_board, wall_mode, current_player, selected_pawn):
    x, y = event.x // 40, event.y // 40  # Convert pixel coordinates to board grid indices
    grid_x, grid_y = (x - 1) // 2, (y - 1) // 2  # Correct grid indices for wall placement

    if wall_mode.get():
        # Determine orientation and adjust grid coordinates for walls
        if x % 2 == 1 and y % 2 == 0:  # Vertical wall
            orientation = 'v'
        elif x % 2 == 0 and y % 2 == 1:  # Horizontal wall
            orientation = 'h'
        else:
            print("Invalid position for wall placement.")
            return

        if game_board.can_place_wall((grid_x, grid_y), orientation):
            if game_board.place_wall((grid_x, grid_y), orientation, current_player.get()):
                draw_board(canvas, game_board)
                current_player.set(1 - current_player.get())  # Switch turns
            else:
                print("Cannot place wall here.")
        else:
            print("Invalid wall position.")
    else:
        # Pawn movement handling
        if selected_pawn[0] is None:
            for idx, (px, py) in enumerate(game_board.pawns):
                if px == x and py == y:
                    selected_pawn[0] = idx
                    break

        if selected_pawn[0] is not None:
            pawn_index = selected_pawn[0]
            current_x, current_y = game_board.pawns[pawn_index]
            direction = determine_direction(x, y, current_x, current_y)

            # Move the pawn if the direction is valid and the move is legal
            if direction and game_board.is_move_legal(pawn_index, direction):
                if game_board.move_pawn(pawn_index, direction):
                    draw_board(canvas, game_board)
                    current_player.set(1 - current_player.get())  # Switch turns after move
                    selected_pawn[0] = None  # Deselect pawn
                else:
                    print("Move could not be performed.")
            else:
                print("Illegal move or not your turn.")
        draw_board(canvas, game_board, selected_pawn[0])

def start_game(root, num_pawns_var, player_types_var, wall_mode_var, current_player):
    print("Game settings:")
    print(f"Number of pawns: {num_pawns_var.get()}")
    for i in range(int(num_pawns_var.get())):
        print(f"Player {i + 1}: {'Bot' if player_types_var[i].get() == 1 else 'Human'}")

    root.withdraw()  # Hide the initial setup window

    game_window = tk.Toplevel(root)
    game_window.title("Quoridor Game Board")
    game_board = GameBoard()
    canvas = tk.Canvas(game_window, width=360, height=360)
    canvas.pack()

    selected_pawn = [None]  # Track the selected pawn

    # Label to show current player
    player_turn_label = tk.Label(game_window, text="Player 1's Turn", font=("Arial", 16))
    player_turn_label.pack()

    def update_player_turn_label():
        player_turn_label.config(text=f"Player {current_player.get() + 1}'s Turn")

    draw_board(canvas, game_board)  # Initial drawing of the board

    # Bind the "W" key to toggle wall mode
    game_window.bind("<Key-w>", lambda event: toggle_wall_mode(wall_mode_var))

    # Ensure canvas updates are linked to current settings and players
    canvas.bind("<Button-1>", lambda event, c=canvas, g=game_board, wm=wall_mode_var, cp=current_player, sp=selected_pawn: on_board_click(event, c, g, wm, cp, sp))
    
    # Update player turn label after every click
    game_window.bind("<Button-1>", lambda event: update_player_turn_label())

    game_window.focus_set()  # Focus on the new window to ensure key events are captured

    def on_close():
        root.quit()  # Terminate the Tkinter mainloop
        root.destroy()  # Destroy the root window

    game_window.protocol("WM_DELETE_WINDOW", on_close)

def setup_game(root):
    frame_controls = tk.Frame(root)
    frame_controls.pack(pady=10)

    # Initialize variables for player turn and wall mode
    current_player = tk.IntVar(value=0)  # 0 for player 1's turn, 1 for player 2's turn
    wall_mode_var = tk.BooleanVar(value=False)  # Track wall mode state

    # Setup for selecting number of pawns and player types
    frame_num_pawns = tk.Frame(root)
    frame_num_pawns.pack(pady=10)

    label_num_pawns = tk.Label(frame_num_pawns, text="Select the number of pawns:")
    label_num_pawns.pack(side=tk.LEFT)

    num_pawns_var = tk.StringVar(root)
    num_pawns_var.set("2")  # Default value

    num_pawns_options = ["2", "4"]
    num_pawns_menu = tk.OptionMenu(frame_num_pawns, num_pawns_var, *num_pawns_options)
    num_pawns_menu.pack(side=tk.LEFT)

    frame_player_types = tk.Frame(root)
    frame_player_types.pack(pady=10)

    player_types_var = [tk.IntVar(value=0) for _ in range(4)]
    player_checkbuttons = []

    for i in range(4):
        cb = tk.Checkbutton(frame_player_types, text=f"Player {i + 1} Bot", variable=player_types_var[i])
        cb.pack(side=tk.LEFT)
        player_checkbuttons.append(cb)

    num_pawns_var.trace('w', lambda *args: update_player_options(num_pawns_var, player_checkbuttons))
    update_player_options(num_pawns_var, player_checkbuttons)

    # Button to start the game, which creates the game window and starts the game
    start_button = tk.Button(root, text="Start Game",
                             command=lambda: start_game(root, num_pawns_var, player_types_var, wall_mode_var,
                                                        current_player))
    start_button.pack(pady=20)
