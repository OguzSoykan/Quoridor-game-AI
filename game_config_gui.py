import tkinter as tk
from tkinter import messagebox
from game_board import GameBoard

def toggle_wall_mode(wall_mode_var, button=None):
    wall_mode_var.set(not wall_mode_var.get())
    if button:
        button.config(text="Wall Mode: " + ("On" if wall_mode_var.get() else "Off"))

def update_player_options(num_pawns_var, player_checkbuttons):
    num_pawns = int(num_pawns_var.get())
    for i in range(4):
        player_checkbuttons[i].config(state='normal' if i < num_pawns else 'disabled')

# game_config_gui.py

def draw_board(canvas, game_board, selected_pawn=None):
    canvas.delete("all")

    # Draw tiles
    for i in range(9):
        for j in range(9):
            canvas.create_rectangle(i * 40, j * 40, (i + 1) * 40, (j + 1) * 40, outline="black", fill="white")

    # Highlight potential moves for the selected pawn
    if selected_pawn is not None:
        x, y = game_board.pawns[selected_pawn]
        player_color = "blue" if selected_pawn == 0 else "yellow"
        for direction in ['up', 'down', 'left', 'right']:
            print(f"Checking potential move {direction} for pawn {selected_pawn} at ({x}, {y})")
            if game_board.is_move_legal(selected_pawn, direction):
                if direction == 'up':
                    print(f"Drawing up move for pawn {selected_pawn} at ({x}, {y - 1})")
                    canvas.create_rectangle(x * 40 + 10, (y - 1) * 40 + 10, x * 40 + 30, y * 40 - 10, outline=player_color, fill=player_color, stipple="gray50")
                elif direction == 'down':
                    print(f"Drawing down move for pawn {selected_pawn} at ({x}, {y + 1})")
                    canvas.create_rectangle(x * 40 + 10, (y + 1) * 40 + 10, x * 40 + 30, (y + 1) * 40 + 30, outline=player_color, fill=player_color, stipple="gray50")
                elif direction == 'left':
                    print(f"Drawing left move for pawn {selected_pawn} at ({x - 1}, {y})")
                    canvas.create_rectangle((x - 1) * 40 + 10, y * 40 + 10, x * 40 - 10, y * 40 + 30, outline=player_color, fill=player_color, stipple="gray50")
                elif direction == 'right':
                    print(f"Drawing right move for pawn {selected_pawn} at ({x + 1}, {y})")
                    canvas.create_rectangle((x + 1) * 40 + 10, y * 40 + 10, (x + 1) * 40 + 30, y * 40 + 30, outline=player_color, fill=player_color, stipple="gray50")

    # Draw pawns (draw after potential moves to avoid overlaps)
    for idx, (x, y) in enumerate(game_board.pawns):
        fill_color = "black" if idx == 0 else "red"
        canvas.create_oval(x * 40 + 10, y * 40 + 10, x * 40 + 30, y * 40 + 30, fill=fill_color)

    # Draw walls (draw after pawns to avoid overlaps)
    for (wx, wy, orientation, player_index) in game_board.walls:
        color = "blue" if player_index == 0 else "red"
        if orientation == 'h':
            canvas.create_line(wx * 40 + 5, wy * 40 + 40, wx * 40 + 75, wy * 40 + 40, fill=color, width=4)
        elif orientation == 'v':
            canvas.create_line(wx * 40 + 40, wy * 40 + 5, wx * 40 + 40, wy * 40 + 75, fill=color, width=4)

    # Draw temporary wall
    if game_board.temp_wall:
        wx, wy, orientation = game_board.temp_wall
        if orientation == 'h':
            canvas.create_line(wx * 40 + 5, wy * 40 + 40, wx * 40 + 75, wy * 40 + 40, fill="green", width=4, dash=(2, 2))
        elif orientation == 'v':
            canvas.create_line(wx * 40 + 40, wy * 40 + 5, wx * 40 + 40, wy * 40 + 75, fill="green", width=4, dash=(2, 2))

    print("Finished drawing the board and potential moves.")




def determine_direction(x, y, current_x, current_y):
    if x == current_x and y == current_y - 1:
        return 'up'
    elif x == current_x and y == current_y + 1:
        return 'down'
    elif x == current_x - 1 and y == current_y:
        return 'left'
    elif x == current_x + 1 and y == current_y:
        return 'right'
    return None

def on_board_click(event, canvas, game_board, wall_mode, current_player, selected_pawn, game_window):
    x, y = event.x // 40, event.y // 40  # Convert pixel coordinates to grid indices

    if wall_mode.get():
        game_board.toggle_temp_wall(x, y)
        draw_board(canvas, game_board)
    else:
        # Pawn movement handling
        if selected_pawn[0] is None:
            for idx, (px, py) in enumerate(game_board.pawns):
                if px == x and py == y:
                    if idx != current_player.get():
                        messagebox.showerror("Invalid Move", "It's not your turn!")
                        return
                    selected_pawn[0] = idx
                    draw_board(canvas, game_board, selected_pawn[0])  # Highlight potential moves
                    return

        if selected_pawn[0] is not None:
            pawn_index = selected_pawn[0]
            if pawn_index != current_player.get():
                messagebox.showerror("Invalid Move", "It's not your turn!")
                selected_pawn[0] = None
                return

            current_x, current_y = game_board.pawns[pawn_index]
            if (x, y) == (current_x, current_y):
                messagebox.showerror("Invalid Move", "You must move to a different position.")
                selected_pawn[0] = None
                return

            direction = determine_direction(x, y, current_x, current_y)

            if direction and game_board.is_move_legal(pawn_index, direction):
                if game_board.move_pawn(pawn_index, direction):
                    draw_board(canvas, game_board)
                    winner = game_board.check_winner()
                    if winner is not None:
                        messagebox.showinfo("Game Over", f"Player {winner + 1} wins!")
                        game_window.quit()
                        game_window.destroy()
                        return
                    current_player.set(1 - current_player.get())  # Switch turns after move
                    selected_pawn[0] = None  # Deselect pawn
                else:
                    messagebox.showerror("Invalid Move", "Move could not be performed.")
            else:
                messagebox.showerror("Invalid Move", "Illegal move or not your turn.")
                selected_pawn[0] = None  # Reset the selected pawn if the move is invalid
        draw_board(canvas, game_board, selected_pawn[0])

def start_game(root, num_pawns_var, player_types_var, wall_mode_var, current_player):
    for i in range(int(num_pawns_var.get())):
        pass

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

    # Add a button to toggle wall mode
    wall_mode_button = tk.Button(game_window, text="Wall Mode: Off", command=lambda: toggle_wall_mode(wall_mode_var, wall_mode_button))
    wall_mode_button.pack()

    # Ensure canvas updates are linked to current settings and players
    canvas.bind("<Button-1>", lambda event, c=canvas, g=game_board, wm=wall_mode_var, cp=current_player, sp=selected_pawn: on_board_click(event, c, g, wm, cp, sp, game_window))
    
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


