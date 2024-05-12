import tkinter as tk
from game_config_gui import setup_game

def main():
    root = tk.Tk()
    root.title("Quoridor Game")
    setup_game(root)
    root.mainloop()

if __name__ == "__main__":
    main()-