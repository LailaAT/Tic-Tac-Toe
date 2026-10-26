# tic-tac-toe game
# GUI -> tkinter

import tkinter as tk
from tkinter import font
from Game import TicTacToeGame
from Move import Move

# board class
class Board(tk.Tk):
    def __init__(self, game: TicTacToeGame):
        super().__init__()
        self.title("Tic Tac Toe")
        self._cells = {}
        self._game = game
        self._create_menu() # call method to create the menu
        self._create_board_display() # call method to create the display
        self._create_grid() # call method to create the grid

    # method to create the display
    def _create_board_display(self):
        display_frame = tk.Frame(master=self) # frame to hold display
        display_frame.pack(fill=tk.X) # geometry manager to fill the frame horizontally
        self.display = tk.Label(
            master=display_frame,
            text="Ready?", # initial text
            font=font.Font(size=28, weight="bold")
        )
        self.display.pack()
    
    
    # method to create the board
    def _create_grid(self):
        grid_frame = tk.Frame(master=self) # frame to hold the grid
        grid_frame.pack() # geometry manager to pack the frame
            
        for row in range(self._game.board_size): # loop through rows (3x3 grid)
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            
            for col in range(self._game.board_size): # loop through columns
                button = tk.Button( # creating a button object for every cell (9 total buttons)
                    master = grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                    highlightthickness=2,
                )
                self._cells[button] = (row, col) # add every button to dict
                button.bind("<Button-1>", self.play) # bind left mouse click to play method
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )
    
    # method for playing
    def play(self, event):
        """Handles player moves"""
        clicked_btn = event.widget # get the button that was clicked
        row, col = self._cells[clicked_btn] # get the row and column of the clicked button
        move = Move(row, col, self._game.current_player.label) # create a Move object with the current player's label
        if self._game.is_valid_move(move): # check if the move is valid
            self._update_button(clicked_btn)
            self._game.process_move(move)
            
            if self._game.is_tied():
                self._update_display(msg="It's a tie!", color="purple")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" wins!'
                color = self._game.current_player.color
                self._update_display(msg=msg, color=color)
            else:
                self._game.toggle_player()
                msg = f'Player "{self._game.current_player.label}" turn'
                self._update_display(msg=msg)
    
    def _update_button(self, button):
        button.config(text=self._game.current_player.label)
        button.config(fg=self._game.current_player.color)
    
    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color
    
    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(bg="lightgreen")
    
    # creating a menu to allow the game to be repeated
    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(
            label="New Game",
            command = self.reset_board
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
    
    def reset_board(self):
        self._game.reset_board()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(text="", highlightbackground="lightblue", fg="black")