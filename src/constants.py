from enum import Enum, auto

class Player(Enum):
    EMPTY = 0
    HUMAN = 1
    AI = 2

class GameState(Enum):
    PLAYING = auto()
    HUMAN_WIN = auto()
    AI_WIN = auto()
    DRAW = auto()

class Direction(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()
    DIAGONAL_MAIN = auto()
    DIAGONAL_COUNTER = auto() 

class GameConfig:
    WIDTH = 800
    HEIGHT = 800
    BOARD_SIZE = 15  # 15x15 board
    SQUARE_SIZE = WIDTH // BOARD_SIZE
    CIRCLE_RADIUS = SQUARE_SIZE // 3
    CIRCLE_WIDTH = 4
    CROSS_WIDTH = 4
    SPACE = SQUARE_SIZE // 4
    LINE_WIDTH = 2
    WIN_LENGTH = 5
    
    class Colors:
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        GREEN = (0, 255, 0)
        YELLOW = (255, 255, 0)
        LIGHT_GRAY = (220, 220, 220)
        GRAY = (128, 128, 128)
        LIGHT_BUTTON = (200, 200, 200)
    class AI:
        EASY_DEPTH = 1
        MEDIUM_DEPTH = 2
        HARD_DEPTH = 3
        MAX_SEARCH_POSITIONS = 20