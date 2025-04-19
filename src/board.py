import pygame
from src.constants import GameConfig, Player

class GameBoard:
    def __init__(self, screen):
        self.screen = screen
        
    def draw_board(self):
        for i in range(1, GameConfig.BOARD_SIZE):
            pygame.draw.line(
                self.screen, 
                GameConfig.Colors.BLACK, 
                (i * GameConfig.SQUARE_SIZE, 0), 
                (i * GameConfig.SQUARE_SIZE, GameConfig.HEIGHT), 
                GameConfig.LINE_WIDTH
            )
        
        for i in range(1, GameConfig.BOARD_SIZE):
            pygame.draw.line(
                self.screen, 
                GameConfig.Colors.BLACK, 
                (0, i * GameConfig.SQUARE_SIZE), 
                (GameConfig.WIDTH, i * GameConfig.SQUARE_SIZE), 
                GameConfig.LINE_WIDTH
            )
    
    def draw_figures(self, board):
        for row in range(GameConfig.BOARD_SIZE):
            for col in range(GameConfig.BOARD_SIZE):
                center_x = int(col * GameConfig.SQUARE_SIZE + GameConfig.SQUARE_SIZE // 2)
                center_y = int(row * GameConfig.SQUARE_SIZE + GameConfig.SQUARE_SIZE // 2)
                
                if board[row][col] == Player.HUMAN.value:
                    pygame.draw.line(
                        self.screen, 
                        GameConfig.Colors.RED,
                        (col * GameConfig.SQUARE_SIZE + GameConfig.SPACE, row * GameConfig.SQUARE_SIZE + GameConfig.SPACE),
                        ((col + 1) * GameConfig.SQUARE_SIZE - GameConfig.SPACE, (row + 1) * GameConfig.SQUARE_SIZE - GameConfig.SPACE),
                        GameConfig.CROSS_WIDTH
                    )
                    pygame.draw.line(
                        self.screen, 
                        GameConfig.Colors.RED,
                        ((col + 1) * GameConfig.SQUARE_SIZE - GameConfig.SPACE, row * GameConfig.SQUARE_SIZE + GameConfig.SPACE),
                        (col * GameConfig.SQUARE_SIZE + GameConfig.SPACE, (row + 1) * GameConfig.SQUARE_SIZE - GameConfig.SPACE),
                        GameConfig.CROSS_WIDTH
                    )
                    
                elif board[row][col] == Player.AI.value:
                    pygame.draw.circle(
                        self.screen,
                        GameConfig.Colors.BLUE,
                        (center_x, center_y),
                        GameConfig.CIRCLE_RADIUS,
                        GameConfig.CIRCLE_WIDTH
                    )
    
    def highlight_winner(self, win_positions):
        for pos in win_positions:
            row, col = pos
            pygame.draw.rect(
                self.screen, 
                GameConfig.Colors.GREEN,
                (col * GameConfig.SQUARE_SIZE, row * GameConfig.SQUARE_SIZE, 
                 GameConfig.SQUARE_SIZE, GameConfig.SQUARE_SIZE),
                5
            )
    
    def highlight_last_move(self, last_move):
        if last_move:
            row, col = last_move
            pygame.draw.rect (
                self.screen, 
                GameConfig.Colors.YELLOW,
                (col * GameConfig.SQUARE_SIZE, row * GameConfig.SQUARE_SIZE, 
                 GameConfig.SQUARE_SIZE, GameConfig.SQUARE_SIZE),
                3
            )