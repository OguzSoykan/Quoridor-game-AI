import tkinter as tk
from game_board import GameBoard

def toggle_wall_mode(wall_mode_var, button):
    wall_mode_var.set(not wall_mode_var.get())
    button.config(text="Wall Mode: " + ("On" if wall_mode_var.get() else "Off"))

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


def on_board_click(event, canvas, game_board, wall_mode, current_player):
    x, y = event.x // 40, event.y // 40  # Convert click position to board coordinates
    if wall_mode.get():
        orientation = 'h' if y % 2 == 1 else 'v'  # Simplify orientation logic; needs adjustment for actual gameplay
        if game_board.place_wall((x, y), orientation):
            draw_board(canvas, game_board)
            current_player.set(1 - current_player.get())  # Toggle between 0 and 1 for two players
        else:
            print("Cannot place wall here")
    else:
        pawn_index = current_player.get()  # Determine which pawn to move based on the current player
        current_x, current_y = game_board.pawns[pawn_index]
        move_direction = determine_direction(x, y, current_x, current_y)
        if move_direction and game_board.is_move_legal(pawn_index, move_direction):
            game_board.move_pawn(pawn_index, move_direction)
            draw_board(canvas, game_board)
            current_player.set(1 - current_player.get())  # Toggle to the next player's turn after a valid move
        else:
            print("Illegal move or not your turn")

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

def start_game(root, num_pawns_var, player_types_var):
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

    canvas.bind("<Button-1>", lambda event, c=canvas, g=game_board: on_board_click(event, c, g))

def setup_game(root):
    frame_controls = tk.Frame(root)
    frame_controls.pack(pady=10)

    current_player = tk.IntVar(value=0)  # 0 for player 1's turn, 1 for player 2's turn

    wall_mode_var = tk.BooleanVar(value=False)
    wall_mode_button = tk.Button(frame_controls, text="Wall Mode: Off",
                                 command=lambda: toggle_wall_mode(wall_mode_var, wall_mode_button))
    wall_mode_button.pack()

    game_window = tk.Toplevel(root)
    game_board = GameBoard()
    canvas = tk.Canvas(game_window, width=360, height=360)
    canvas.pack()
    draw_board(canvas, game_board)
    canvas.bind("<Button-1>", lambda event, c=canvas, g=game_board, wm=wall_mode_var, cp=current_player: on_board_click(event, c, g, wm, cp))
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

    start_button = tk.Button(root, text="Start Game", command=lambda: start_game(root, num_pawns_var, player_types_var))
    start_button.pack(pady=20)