import tkinter as tk

def update_player_options(*args):
    # Update player type options based on the number of pawns selected
    num_pawns = int(num_pawns_var.get())
    for i in range(4):
        player_checkbuttons[i].config(state='normal' if i < num_pawns else 'disabled')

def start_game():
    print("Game settings:")
    print(f"Number of pawns: {num_pawns_var.get()}")
    for i in range(int(num_pawns_var.get())):
        print(f"Player {i+1}: {'Bot' if player_types_var[i].get() == 1 else 'Human'}")
    # Here you would add the code to initialize and start the game based on these settings

root = tk.Tk()
root.title("Quoridor Game Setup")

# Create a frame for the number of pawns selection
frame_num_pawns = tk.Frame(root)
frame_num_pawns.pack(pady=10)

label_num_pawns = tk.Label(frame_num_pawns, text="Select the number of pawns:")
label_num_pawns.pack(side=tk.LEFT)

num_pawns_var = tk.StringVar(root)
num_pawns_var.set("2")  # default value
num_pawns_var.trace('w', update_player_options)
num_pawns_options = ["2", "4"]
num_pawns_menu = tk.OptionMenu(frame_num_pawns, num_pawns_var, *num_pawns_options)
num_pawns_menu.pack(side=tk.LEFT)

# Create a frame for player type options
frame_player_types = tk.Frame(root)
frame_player_types.pack(pady=10)

player_types_var = [tk.IntVar(value=0) for _ in range(4)]
player_checkbuttons = []

for i in range(4):
    cb = tk.Checkbutton(frame_player_types, text=f"Player {i+1} Bot", variable=player_types_var[i])
    cb.pack(side=tk.LEFT)
    player_checkbuttons.append(cb)

# Disable irrelevant player checkboxes initially
update_player_options()

# Button to start the game
start_button = tk.Button(root, text="Start Game", command=start_game)
start_button.pack(pady=20)

# Run the main loop
root.mainloop()
