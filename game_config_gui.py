import tkinter as tk
from game_board import GameBoard

def toggle_wall_mode(wall_mode_var, button=None):
    wall_mode_var.set(not wall_mode_var.get())
    if button:
        button.config(text="Wall Mode: " + ("On" if wall_mode_var.get() else "Off"))
    print("Wall Mode: " + ("On" if wall_mode_var.get() else "Off"))  # For console feedback

def update_player_options(num_pawns_var, player_checkbuttons):
    num_pawns = int(num_pawns_var.get())
    for i in range(4):
        player_checkbuttons[i].config(state='normal' if i < num_pawns else 'disabled')

def draw_board(canvas, game_board):
    canvas.delete("all")
    for i in range(9):
        for j in range(9):
            canvas.create_rectangle(i*40, j*40, (i+1)*40, (j+1)*40, outline="black", fill="white")
    for idx, (x, y) in enumerate(game_board.pawns):
        fill_color = "black" if idx == 0 else "red"  # Distinguish different players
        canvas.create_oval(x*40+10, y*40+10, x*40+30, y*40+30, fill=fill_color)
    for (wx, wy, orientation) in game_board.walls:
        if orientation == 'h':
            canvas.create_line(wx*40, wy*40+20, (wx+1)*40+40, wy*40+20, fill="blue", width=4)
        elif orientation == 'v':
            canvas.create_line(wx*40+20, wy*40, wx*40+20, (wy+1)*40+40, fill="blue", width=4)

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

def on_board_click(event, canvas, game_board, wall_mode, current_player):
    x, y = event.x // 40, event.y // 40  # Convert pixel coordinates to grid indices
    grid_x, grid_y = x // 2, y // 2  # Adjust to grid coordinates for wall placement

    if wall_mode.get():
        # Determine orientation based on mouse click: Vertical if odd x; horizontal if odd y
        if x % 2 == 1:  # Assumes vertical wall when clicking on the odd indexed x
            orientation = 'v'
        elif y % 2 == 1:  # Assumes horizontal wall when clicking on the odd indexed y
            orientation = 'h'
        else:
            print("Invalid position for wall placement.")
            return  # Exit the function if neither condition is true

        if game_board.can_place_wall((grid_x, grid_y), orientation):
            if game_board.place_wall((grid_x, grid_y), orientation):
                draw_board(canvas, game_board)
            else:
                print(f"{orientation.upper()} wall cannot be placed here.")
        else:
            print(f"Cannot place a {orientation.upper()} wall at ({grid_x}, {grid_y}).")
    else:
        pawn_index = current_player.get()  # Determine which pawn to move based on the current player
        current_x, current_y = game_board.pawns[pawn_index]
        move_direction = determine_direction(x, y, current_x, current_y)
        if move_direction and game_board.is_move_legal(pawn_index, move_direction):
            if game_board.move_pawn(pawn_index, move_direction):
                draw_board(canvas, game_board)
                current_player.set(1 - current_player.get())  # Toggle to the next player's turn after a valid move
            else:
                print("Move could not be performed.")
        else:
            print("Illegal move or not your turn")

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

    draw_board(canvas, game_board)  # Initial drawing of the board

    # Bind the "W" key to toggle wall mode
    game_window.bind("<Key-w>", lambda event: toggle_wall_mode(wall_mode_var))

    # Ensure canvas updates are linked to current settings and players
    canvas.bind("<Button-1>", lambda event, c=canvas, g=game_board, wm=wall_mode_var, cp=current_player: on_board_click(event, c, g, wm, cp))

    game_window.focus_set()  # Focus on the new window to ensure key events are captured

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
