from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QPixmap
import sys
import tkinter as tk
from tkinter import messagebox
from game_board import GameBoard
from game_config_gui import draw_board, on_board_click
from player import Player
import time
from bot_ai import bot_decision

from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.player1Image.setPixmap(QPixmap("images/player1.png"))
        self.ui.player2Image.setPixmap(QPixmap("images/player2.png"))
        self.ui.botImage.clear() # while creating on qt creator I put text to not confuse, and I dont want it show on start screen
        self.setWindowIcon(QPixmap("images/multi_pawn_icon.png")) # set window icon

        self.player1_var = 0    # Always human, so 0
        self.player2_var = self.ui.player2Box.currentIndexChanged.connect(self.comboBoxChanged)

        self.ui.startButton.clicked.connect(self.start_game)  # start button
        self.ui.exitButton.clicked.connect(sys.exit)  # exit button

    def comboBoxChanged(self):
        if self.ui.player2Box.currentIndex() == 0:
            self.ui.botImage.clear() # clear bot image after human is selected
            return 0
        elif self.ui.player2Box.currentIndex() == 1:
            self.ui.botImage.setPixmap(QPixmap("images/bot.png"))  # show bot image if bot is selected
            return 1

    def start_game(self):
        player_types = [self.player1_var, self.comboBoxChanged()]  # store player types chosen
        self.main_game(player_types)

    def main_game(self, player_types):
        self.close()

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
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
