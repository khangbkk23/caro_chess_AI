import pygame
from src.constants import GameConfig, Player, GameState

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 32)
        self.small_font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.restart_rect = None
        self.difficulty_buttons = []
        self.setup_difficulty_buttons()
        
    def setup_difficulty_buttons(self):
        button_width = 150
        button_height = 50
        spacing = 20
        total_width = 3 * button_width + 2 * spacing
        start_x = (GameConfig.WIDTH - total_width) // 2
        start_y = GameConfig.HEIGHT // 2
        
        self.difficulty_buttons = [
            {
                "rect": pygame.Rect(start_x, start_y, button_width, button_height),
                "text": "Easy",
                "value": GameConfig.AI.EASY_DEPTH,
                "description": "Quick moves"
            },
            {
                "rect": pygame.Rect(start_x + button_width + spacing, start_y, button_width, button_height),
                "text": "Medium",
                "value": GameConfig.AI.MEDIUM_DEPTH,
                "description": "Balance"
            },
            {
                "rect": pygame.Rect(start_x + 2 * (button_width + spacing), start_y, button_width, button_height),
                "text": "Hard",
                "value": GameConfig.AI.HARD_DEPTH,
                "description": "Challenging"
            }
        ]
        
    def draw_difficulty_menu(self):
        # Draw title
        title_text = self.title_font.render("Caro Game", True, GameConfig.Colors.BLUE)
        title_rect = title_text.get_rect(center=(GameConfig.WIDTH//2, GameConfig.HEIGHT//4))
        self.screen.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = self.font.render("Select Difficulty Level", True, GameConfig.Colors.BLACK)
        subtitle_rect = subtitle_text.get_rect(center=(GameConfig.WIDTH//2, GameConfig.HEIGHT//3))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw difficulty buttons
        for button in self.difficulty_buttons:
            color = GameConfig.Colors.LIGHT_BUTTON
            text_color = GameConfig.Colors.BLACK
            border_color = GameConfig.Colors.GRAY
            
            pygame.draw.rect(self.screen, color, button["rect"], border_radius=10)
            pygame.draw.rect(self.screen, border_color, button["rect"], 2, border_radius=10)
            
            text_surface = self.font.render(button["text"], True, text_color)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)
            
            # Draw description
            desc_surface = self.small_font.render(button["description"], True, GameConfig.Colors.GRAY)
            desc_rect = desc_surface.get_rect(center=(button["rect"].centerx, button["rect"].bottom + 20))
            self.screen.blit(desc_surface, desc_rect)
        
    def draw_status(self, game_state, current_player, current_difficulty):
        status_rect = pygame.Rect(0, 0, GameConfig.WIDTH, 40)
        pygame.draw.rect(self.screen, GameConfig.Colors.LIGHT_GRAY, status_rect)
        
        # Game status text
        if game_state != GameState.PLAYING:
            if game_state == GameState.HUMAN_WIN:
                text = "You Win!"
                color = GameConfig.Colors.RED
            elif game_state == GameState.AI_WIN:
                text = "AI Wins!"
                color = GameConfig.Colors.BLUE
            else:  # Draw
                text = "Draw!"
                color = GameConfig.Colors.GRAY
            
            text_surface = self.font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(GameConfig.WIDTH//2, 20))
            self.screen.blit(text_surface, text_rect)
            
            restart_text = self.font.render("Play Again", True, GameConfig.Colors.BLACK)
            self.restart_rect = restart_text.get_rect(center=(GameConfig.WIDTH//2, GameConfig.HEIGHT - 30))
            pygame.draw.rect(
                self.screen, 
                GameConfig.Colors.LIGHT_BUTTON, 
                self.restart_rect.inflate(20, 10), 
                border_radius=5
            )
            self.screen.blit(restart_text, self.restart_rect)
        else:
            if current_player == Player.HUMAN:
                text = "Your Turn (X)"
                color = GameConfig.Colors.RED
            else:
                text = "AI's Turn (O)"
                color = GameConfig.Colors.BLUE
            
            text_surface = self.font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(GameConfig.WIDTH//2, 20))
            self.screen.blit(text_surface, text_rect)
        
        if current_difficulty is not None:
            diff_text = f"Difficulty: {self.get_difficulty_name(current_difficulty)}"
            diff_surface = self.small_font.render(diff_text, True, GameConfig.Colors.BLACK)
            self.screen.blit(diff_surface, (10, GameConfig.HEIGHT - 30))
    
    def get_difficulty_name(self, difficulty_value):
        for button in self.difficulty_buttons:
            if button["value"] == difficulty_value:
                return button["text"]
        return "Custom"