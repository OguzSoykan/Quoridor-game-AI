import tkinter as tk
from tkinter import messagebox

from game_board import GameBoard
from game_config_gui import draw_board, on_board_click

def main():
    game_window = tk.Tk()
    game_window.title("Quoridor Game")

    canvas = tk.Canvas(game_window, width=400, height=400)
    canvas.pack()

    game_board = GameBoard()
    wall_mode = tk.BooleanVar()
    wall_mode.set(False)
    current_player = tk.IntVar()
    current_player.set(0)
    selected_pawn = [None]

    def toggle_wall_mode():
        wall_mode.set(not wall_mode.get())

    wall_button = tk.Button(game_window, text="Place Wall", command=toggle_wall_mode)
    wall_button.pack()

    def confirm_wall_placement():
        if game_board.temp_wall:
            player = game_board.players[current_player.get()]
            if player.wall_count > 0:
                if game_board.confirm_wall(current_player.get()):
                    draw_board(canvas, game_board)
                    switch_turn()
                    selected_pawn[0] = None
                    wall_mode.set(False)  # Exit wall mode after confirming wall
                else:
                    messagebox.showerror("Invalid Move", "Cannot place wall here.")
            else:
                messagebox.showinfo("No Walls Left", "You have no walls left.")
        else:
            messagebox.showinfo("No Wall", "No temporary wall to confirm.")

    confirm_button = tk.Button(game_window, text="Confirm Wall Placement", command=confirm_wall_placement)
    confirm_button.pack()

    def cancel_wall_placement():
        if game_board.temp_wall:
            game_board.temp_wall = None
            draw_board(canvas, game_board)
        wall_mode.set(False)  # Exit wall mode

    cancel_button = tk.Button(game_window, text="Cancel Wall Placement", command=cancel_wall_placement)
    cancel_button.pack()

    def on_canvas_click(event):
        on_board_click(event, canvas, game_board, wall_mode, current_player, selected_pawn, game_window)
        update_player_turn_label()

    canvas.bind("<Button-1>", on_canvas_click)

    # Label to show current player
    player_turn_label = tk.Label(game_window, text="Player 1's Turn", font=("Arial", 16))
    player_turn_label.pack()

    def update_player_turn_label():
        player_turn_label.config(text=f"Player {current_player.get() + 1}'s Turn")

    def switch_turn():
        current_player.set(1 - current_player.get())
        update_player_turn_label()

    draw_board(canvas, game_board)
    game_window.mainloop()

if __name__ == "__main__":
    main()
