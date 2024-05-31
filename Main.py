import tkinter as tk
from tkinter import messagebox
from game_board import GameBoard
from game_config_gui import draw_board, on_board_click
from player import Player
import time
from bot_ai import bot_decision

def start_screen():
    def start_game():
        player_types = [player1_var.get(), player2_var.get()]
        start_window.destroy()
        main_game(player_types)

    start_window = tk.Tk()
    start_window.title("Quoridor Game Start Screen")

    label = tk.Label(start_window, text="Welcome to Quoridor!", font=("Arial", 24))
    label.pack(pady=20)

    player1_var = tk.IntVar(value=0)  # 0 for human, 1 for bot
    player2_var = tk.IntVar(value=0)  # 0 for human, 1 for bot

    player1_label = tk.Label(start_window, text="Player 1:", font=("Arial", 16))
    player1_label.pack(pady=10)
    player1_human_radio = tk.Radiobutton(start_window, text="Human", variable=player1_var, value=0, font=("Arial", 14))
    player1_human_radio.pack(pady=5)
    player1_bot_radio = tk.Radiobutton(start_window, text="Bot", variable=player1_var, value=1, font=("Arial", 14))
    player1_bot_radio.pack(pady=5)

    player2_label = tk.Label(start_window, text="Player 2:", font=("Arial", 16))
    player2_label.pack(pady=10)
    player2_human_radio = tk.Radiobutton(start_window, text="Human", variable=player2_var, value=0, font=("Arial", 14))
    player2_human_radio.pack(pady=5)
    player2_bot_radio = tk.Radiobutton(start_window, text="Bot", variable=player2_var, value=1, font=("Arial", 14))
    player2_bot_radio.pack(pady=5)

    start_button = tk.Button(start_window, text="Start Game", command=start_game, font=("Arial", 16))
    start_button.pack(pady=20)

    start_window.mainloop()

def main_game(player_types):
    game_window = tk.Tk()
    game_window.title("Quoridor Game")

    canvas = tk.Canvas(game_window, width=400, height=400)
    canvas.pack()

    game_board = GameBoard(player_types)
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
                    wall_mode.set(False)
                    update_wall_count_labels()
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
        wall_mode.set(False)

    cancel_button = tk.Button(game_window, text="Cancel Wall Placement", command=cancel_wall_placement)
    cancel_button.pack()

    def on_canvas_click(event):
        on_board_click(event, canvas, game_board, wall_mode, current_player, selected_pawn, game_window)
        update_player_turn_label()
        check_ai_turn()

    canvas.bind("<Button-1>", on_canvas_click)

    player_turn_label = tk.Label(game_window, text="Player 1's Turn", font=("Arial", 16))
    player_turn_label.pack()

    wall_count_labels = [
        tk.Label(game_window, text="Player 1 Walls: 10", font=("Arial", 12)),
        tk.Label(game_window, text="Player 2 Walls: 10", font=("Arial", 12))
    ]
    for label in wall_count_labels:
        label.pack()

    def update_wall_count_labels():
        for i, player in enumerate(game_board.players):
            wall_count_labels[i].config(text=f"Player {i + 1} Walls: {player.wall_count}")

    def update_player_turn_label():
        player_turn_label.config(text=f"Player {current_player.get() + 1}'s Turn")

    def switch_turn():
        current_player.set(1 - current_player.get())
        update_player_turn_label()
        check_ai_turn()

    def check_ai_turn():
        player = game_board.players[current_player.get()]
        if player.is_bot:
            game_window.after(1000, execute_bot_move)

    def execute_bot_move():
        player = game_board.players[current_player.get()]
        if player.is_bot:
            best_move = player.make_move(game_board)
            if best_move:
                draw_board(canvas, game_board)
                update_wall_count_labels()
                winner = game_board.check_winner()
                if winner is not None:
                    messagebox.showinfo("Game Over", f"Player {winner + 1} wins!")
                    game_window.quit()
                    game_window.destroy()
                    return
                switch_turn()

    draw_board(canvas, game_board)
    check_ai_turn()  # Check if AI needs to move at the start of the game
    game_window.mainloop()

if __name__ == "__main__":
    start_screen()
