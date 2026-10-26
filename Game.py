from itertools import cycle
from Move import Move
from Player import Player

BOARD_SIZE = 3
DEFAULT_PLAYERS = [Player("X", "red"), Player("O", "blue")]

class TicTacToeGame:
    
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players) # iterates over tuple of players
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = [] # combination of cells that make up the winning combo
        self._current_moves = [] # list of possible moves for a player in a game
        self._has_winner = False
        self._winning_combos = [] # list of all possible winning combinations
        self._setup_board()
        
    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)] 
            for row in range(self.board_size)
        ]
        # create a list of lists 
        # each inner list will contain empty Move objects
        # (where you have the coordinates of the cell and player label)
        self._winning_combos = self._generate_winning_combos()
    
    # there are 8 possible winning combinations in a 3x3 tic-tac-toe game
    def _generate_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        
        columns = [list(col) for col in zip(*rows)]
        
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    # checking if move is valid
    def is_valid_move(self, move):
        """true if valid, false if not"""
        row, col = move.row, move.col
        # checking this move hasn't been played yet
        move_was_not_played = self._current_moves[row][col].label == ""
        # checking that there is no winner yet
        no_winner = not self._has_winner
        return no_winner and move_was_not_played
    
    # checking to see if there is a winner
    def process_move(self, move):
        """Processes current move done by current player to check if it's a winning"""
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            # retrievees all labels from winning combos 
            # (sets don't allow repetition so, if winning, it will onnly yield one X/O)
            results = set(
                self._current_moves[n][m].label
                for n, m in combo
            )
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break
            
    def has_winner(self):
        return self._has_winner
    
    # checking if tied
    def is_tied(self):
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        # if all labels are filled and there is no winner, then it's a tie
        return no_winner and all(played_moves)
    
    def toggle_player(self):
        self.current_player = next(self._players)
    
    def reset_board(self):
        for row, content in enumerate(self._current_moves):
            for col, move in enumerate(content):
                content[col] = Move(row, col, "")
        self._has_winner = False
        self.winner_combo = []

    
