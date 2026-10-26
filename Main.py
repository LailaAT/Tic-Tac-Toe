from Board import Board
from Game import TicTacToeGame

# main method
def main():
    game = TicTacToeGame() # create a Game object
    board = Board(game)
    board.mainloop()

if __name__ == "__main__":
    main()