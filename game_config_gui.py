import tkinter as tk
from game_board import GameBoard

def update_player_options(num_pawns_var, player_checkbuttons):
    num_pawns = int(num_pawns_var.get())
    for i in range(4):
        player_checkbuttons[i].config(state='normal' if i < num_pawns else 'disabled')


def start_game(root, num_pawns_var, player_types_var):
    print("Game settings:")
    print(f"Number of pawns: {num_pawns_var.get()}")
    for i in range(int(num_pawns_var.get())):
        print(f"Player {i + 1}: {'Bot' if player_types_var[i].get() == 1 else 'Human'}")

    # Hide the initial setup window
    root.withdraw()

    # Start the main game window
    game_window = tk.Toplevel(root)
    game_window.title("Quoridor Game Board")
    game_board = GameBoard()  # Assuming GameBoard needs no parameters
    canvas = tk.Canvas(game_window, width=360, height=360)
    canvas.pack()

    # Draw the board
    for i in range(9):
        for j in range(9):
            canvas.create_rectangle(i * 40, j * 40, (i + 1) * 40, (j + 1) * 40, outline="black", fill="white")

    # Draw pawns based on their positions in game_board.pawns
    for x, y in game_board.pawns:
        canvas.create_oval(x * 40 + 10, y * 40 + 10, x * 40 + 30, y * 40 + 30, fill="black")

    # Bind canvas to a click event if you want to move pawns or place walls
    canvas.bind("<Button-1>", lambda event, c=canvas, g=game_board: on_board_click(event, c, g))

def on_board_click(event, canvas, game_board):
    x, y = event.x // 40, event.y // 40  # Convert click position to board coordinates
    print(f"Clicked on: {x}, {y}")
    # Implement logic here to handle the click, move pawns, or place walls


def setup_game(root):
    frame_num_pawns = tk.Frame(root)
    frame_num_pawns.pack(pady=10)

    label_num_pawns = tk.Label(frame_num_pawns, text="Select the number of pawns:")
    label_num_pawns.pack(side=tk.LEFT)

    num_pawns_var = tk.StringVar(root)
    num_pawns_var.set("2")  # default value

    num_pawns_options = ["2", "4"]
    num_pawns_menu = tk.OptionMenu(frame_num_pawns, num_pawns_var, *num_pawns_options)
    num_pawns_menu.pack(side=tk.LEFT)

    frame_player_types = tk.Frame(root)
    frame_player_types.pack(pady=10)

    player_types_var = [tk.IntVar(value=0) for _ in range(4)]
    player_checkbuttons = []

    for i in range(4):
        cb = tk.Checkbutton(frame_player_types, text=f"Player {i+1} Bot", variable=player_types_var[i])
        cb.pack(side=tk.LEFT)
        player_checkbuttons.append(cb)

    num_pawns_var.trace('w', lambda *args: update_player_options(num_pawns_var, player_checkbuttons))
    update_player_options(num_pawns_var, player_checkbuttons)  # Initialize state

    start_button = tk.Button(root, text="Start Game", command=lambda: start_game(root, num_pawns_var, player_types_var))
    start_button.pack(pady=20)
