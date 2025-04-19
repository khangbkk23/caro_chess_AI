import numpy as np
from src.constants import GameConfig, Player, Direction, GameState

class GameLogic:
    def __init__(self):
        self.board = np.zeros((GameConfig.BOARD_SIZE, GameConfig.BOARD_SIZE), dtype=int)
        self.last_move = None
    
    def is_valid_move(self, row, col):
        return (0 <= row < GameConfig.BOARD_SIZE and 
                0 <= col < GameConfig.BOARD_SIZE and 
                self.board[row][col] == Player.EMPTY.value)
    
    def make_move(self, row, col, player):
        self.board[row][col] = player.value
        self.last_move = (row, col)
    
    def check_win(self, player):
        player_value = player.value
        win_length = GameConfig.WIN_LENGTH
        def check_window(positions):
            return all(self.board[r][c] == player_value for r, c in positions)
        
        for direction in Direction:
            if direction == Direction.HORIZONTAL:
                for row in range(GameConfig.BOARD_SIZE):
                    for col in range(GameConfig.BOARD_SIZE - win_length + 1):
                        positions = [(row, col+i) for i in range(win_length)]
                        if check_window(positions):
                            return True, positions
                            
            elif direction == Direction.VERTICAL:
                for row in range(GameConfig.BOARD_SIZE - win_length + 1):
                    for col in range(GameConfig.BOARD_SIZE):
                        positions = [(row+i, col) for i in range(win_length)]
                        if check_window(positions):
                            return True, positions
                            
            elif direction == Direction.DIAGONAL_MAIN:
                for row in range(GameConfig.BOARD_SIZE - win_length + 1):
                    for col in range(GameConfig.BOARD_SIZE - win_length + 1):
                        positions = [(row+i, col+i) for i in range(win_length)]
                        if check_window(positions):
                            return True, positions
                            
            elif direction == Direction.DIAGONAL_COUNTER:
                for row in range(GameConfig.BOARD_SIZE - win_length + 1):
                    for col in range(win_length - 1, GameConfig.BOARD_SIZE):
                        positions = [(row+i, col-i) for i in range(win_length)]
                        if check_window(positions):
                            return True, positions
        
        return False, []
    
    def is_board_full(self):
        return not np.any(self.board == Player.EMPTY.value)