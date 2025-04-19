import pygame
import sys
import time
import numpy as np

from src.constants import GameConfig, Player, GameState
from src.board import GameBoard
from src.game_play import GameLogic
from src.ai_logic import AILogic
from src.UI import UIManager

class CaroGame:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((GameConfig.WIDTH, GameConfig.HEIGHT))
        pygame.display.set_caption('Caro Game - Minimax Alpha-Beta')
        
        self.game_logic = GameLogic()
        self.ai_logic = AILogic(self.game_logic)
        self.board_renderer = GameBoard(self.screen)
        self.ui_manager = UIManager(self.screen)
        
        self.game_state = GameState.PLAYING
        self.current_player = Player.HUMAN
        self.win_positions = []
        self.current_difficulty = None
        self.show_difficulty_menu = True
        self.screen.fill(GameConfig.Colors.WHITE)
        self.board_renderer.draw_board()
    
    def restart(self):
        self.game_logic = GameLogic()
        self.ai_logic = AILogic(self.game_logic)
        self.game_state = GameState.PLAYING
        self.current_player = Player.HUMAN
        self.win_positions = []
        self.show_difficulty_menu = True
        
        self.screen.fill(GameConfig.Colors.WHITE)
        self.board_renderer.draw_board()
    
    def start_game(self, difficulty):
        self.current_difficulty = difficulty
        self.show_difficulty_menu = False
        self.game_state = GameState.PLAYING
        self.current_player = Player.HUMAN
    
    def ai_move(self):
        if self.current_difficulty is None:
            return
            
        piece_count = np.count_nonzero(self.game_logic.board)
        
        # Dynamic depth adjustment based on game phase
        if piece_count < 10:  # Opening phase
            depth = self.current_difficulty
        elif piece_count < 30:  # Midgame
            depth = max(1, self.current_difficulty - 1)
        else:  # Endgame
            depth = max(1, self.current_difficulty - 2)
        
        _, best_move = self.ai_logic.minimax(depth, float('-inf'), float('inf'), True)
        
        if best_move:
            row, col = best_move
            self.game_logic.make_move(row, col, Player.AI)
            
            is_win, win_positions = self.game_logic.check_win(Player.AI)
            if is_win:
                self.game_state = GameState.AI_WIN
                self.win_positions = win_positions
            elif self.game_logic.is_board_full():
                self.game_state = GameState.DRAW
            else:
                self.current_player = Player.HUMAN
    
    def handle_click(self, mouseX, mouseY):
        if self.show_difficulty_menu:
            for button in self.ui_manager.difficulty_buttons:
                if button["rect"].collidepoint(mouseX, mouseY):
                    self.start_game(button["value"])
                    return
            return
        
        if self.game_state != GameState.PLAYING:
            if self.ui_manager.restart_rect and self.ui_manager.restart_rect.collidepoint(mouseX, mouseY):
                self.restart()
                return
            return
        
        if self.current_player != Player.HUMAN:
            return
        
        clicked_row = int(mouseY // GameConfig.SQUARE_SIZE)
        clicked_col = int(mouseX // GameConfig.SQUARE_SIZE)
        
        if self.game_logic.is_valid_move(clicked_row, clicked_col):
            self.game_logic.make_move(clicked_row, clicked_col, Player.HUMAN)
            
            is_win, win_positions = self.game_logic.check_win(Player.HUMAN)
            if is_win:
                self.game_state = GameState.HUMAN_WIN
                self.win_positions = win_positions
            elif self.game_logic.is_board_full():
                self.game_state = GameState.DRAW
            else:
                self.current_player = Player.AI
    
    def update_display(self):
        self.screen.fill(GameConfig.Colors.WHITE)
        
        if self.show_difficulty_menu:
            self.ui_manager.draw_difficulty_menu()
        else:
            self.board_renderer.draw_board()
            self.board_renderer.draw_figures(self.game_logic.board)
            
            if self.win_positions:
                self.board_renderer.highlight_winner(self.win_positions)
            
            if self.game_logic.last_move:
                self.board_renderer.highlight_last_move(self.game_logic.last_move)
            
            self.ui_manager.draw_status(
                self.game_state,
                self.current_player,
                self.current_difficulty
            )
        
        pygame.display.update()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    self.handle_click(mouseX, mouseY)
            
            if (not self.show_difficulty_menu and 
                self.current_player == Player.AI and 
                self.game_state == GameState.PLAYING):
                self.update_display()
                time.sleep(0.5)
                self.ai_move()
            
            self.update_display()


if __name__ == "__main__":
    game = CaroGame()
    game.run()