import random
from src.constants import GameConfig, Player, Direction
from typing import List, Tuple, Optional

class AILogic:
    def __init__(self, game_logic):
        self.game_logic = game_logic
        self.pattern_values = {
            # Winning condition
            (5, 0): 1000000,   # Immediate win
            
            # Offensive patterns
            (4, 0): 50000,      # Open four
            (3, 0): 10000,      # Open three
            (2, 0): 500,        # Open two
            (1, 0): 10,         # Single stone
            
            # Defensive patterns (blocking opponent)
            (0, 4): 40000,      # Block opponent's open four
            (0, 3): 8000,       # Block opponent's open three
            (0, 2): 400,        # Block opponent's open two
            
            # Mixed patterns
            (4, 1): 30000,      # Four with one blocked end
            (3, 1): 7000,      # Three with one blocked end
        }
        
    def evaluate_window(self, window: List[int], player: Player) -> int:
        """Evaluate a window of spaces for scoring potential"""
        player_val = player.value
        opponent_val = Player.HUMAN.value if player == Player.AI else Player.AI.value
        empty = Player.EMPTY.value
        
        player_count = window.count(player_val)
        opponent_count = window.count(opponent_val)
        empty_count = window.count(empty)
        
        # Check for known patterns
        key = (player_count, opponent_count)
        if key in self.pattern_values:
            return self.pattern_values[key]
        
        # Special case: double open three (very strong)
        if player_count == 3 and empty_count == 2:
            # Check if this creates two open threes
            if self._creates_double_open_three(window, player_val):
                return 25000
        
        return 0
    
    def _creates_double_open_three(self, window: List[int], player_val: int) -> bool:
        return window.count(player_val) == 3 and window.count(Player.EMPTY.value) == 2
    
    def score_position(self, player: Player) -> int:
        score = 0
        board = self.game_logic.board
        for direction in Direction:
            if direction == Direction.HORIZONTAL:
                for row in range(GameConfig.BOARD_SIZE):
                    for col in range(GameConfig.BOARD_SIZE - GameConfig.WIN_LENGTH + 1):
                        window = [board[row][col+i] for i in range(GameConfig.WIN_LENGTH)]
                        score += self.evaluate_window(window, player)
                        
            elif direction == Direction.VERTICAL:
                for col in range(GameConfig.BOARD_SIZE):
                    for row in range(GameConfig.BOARD_SIZE - GameConfig.WIN_LENGTH + 1):
                        window = [board[row+i][col] for i in range(GameConfig.WIN_LENGTH)]
                        score += self.evaluate_window(window, player)
                        
            elif direction == Direction.DIAGONAL_MAIN:
                for row in range(GameConfig.BOARD_SIZE - GameConfig.WIN_LENGTH + 1):
                    for col in range(GameConfig.BOARD_SIZE - GameConfig.WIN_LENGTH + 1):
                        window = [board[row+i][col+i] for i in range(GameConfig.WIN_LENGTH)]
                        score += self.evaluate_window(window, player)
                        
            elif direction == Direction.DIAGONAL_COUNTER:
                for row in range(GameConfig.BOARD_SIZE - GameConfig.WIN_LENGTH + 1):
                    for col in range(GameConfig.WIN_LENGTH - 1, GameConfig.BOARD_SIZE):
                        window = [board[row+i][col-i] for i in range(GameConfig.WIN_LENGTH)]
                        score += self.evaluate_window(window, player)
        
        # Center control bonus
        center = GameConfig.BOARD_SIZE // 2
        if board[center][center] == player.value:
            score += 20
            
        # Corner control bonus
        corners = [(0,0), (0, GameConfig.BOARD_SIZE-1), 
                  (GameConfig.BOARD_SIZE-1, 0), (GameConfig.BOARD_SIZE-1, GameConfig.BOARD_SIZE-1)]
        for row, col in corners:
            if board[row][col] == player.value:
                score += 5
                
        return score
    
    def get_adjacent_moves(self) -> List[Tuple[int, int]]:
        """Get all potentially good moves near existing pieces"""
        moves = set()
        board = self.game_logic.board
        directions = [(-1,-1), (-1,0), (-1,1),
                      (0,-1),          (0,1),
                      (1,-1),  (1,0),  (1,1)]
        
        # First look for immediate winning moves or blocks
        for row in range(GameConfig.BOARD_SIZE):
            for col in range(GameConfig.BOARD_SIZE):
                if board[row][col] == Player.EMPTY.value:
                    # Check if this is a winning move for AI
                    board[row][col] = Player.AI.value
                    if self.game_logic.check_win(Player.AI)[0]:
                        board[row][col] = Player.EMPTY.value
                        return [(row, col)]
                    board[row][col] = Player.EMPTY.value
                    
                    # Check if this blocks a human win
                    board[row][col] = Player.HUMAN.value
                    if self.game_logic.check_win(Player.HUMAN)[0]:
                        board[row][col] = Player.EMPTY.value
                        return [(row, col)]
                    board[row][col] = Player.EMPTY.value
        
        # Then collect moves near existing pieces
        for row in range(GameConfig.BOARD_SIZE):
            for col in range(GameConfig.BOARD_SIZE):
                if board[row][col] != Player.EMPTY.value:
                    for dr, dc in directions:
                        for distance in [1, 2]:  # Look 1-2 spaces away
                            r, c = row + dr*distance, col + dc*distance
                            if (0 <= r < GameConfig.BOARD_SIZE and 
                                0 <= c < GameConfig.BOARD_SIZE and 
                                board[r][c] == Player.EMPTY.value):
                                moves.add((r, c))
        
        # If no adjacent moves, start from center
        if not moves:
            center = GameConfig.BOARD_SIZE // 2
            if board[center][center] == Player.EMPTY.value:
                return [(center, center)]
            else:
                # If center taken, pick random adjacent
                return [(center + dr, center + dc) 
                        for dr, dc in directions 
                        if (0 <= center + dr < GameConfig.BOARD_SIZE and 
                            0 <= center + dc < GameConfig.BOARD_SIZE and
                            board[center + dr][center + dc] == Player.EMPTY.value)]
        
        return list(moves)
    
    def minimax(self, depth: int, alpha: float, beta: float, maximizing: bool) -> Tuple[float, Optional[Tuple[int, int]]]:
        """Minimax algorithm with alpha-beta pruning"""
        board = self.game_logic.board
        
        # Check terminal states
        human_wins, _ = self.game_logic.check_win(Player.HUMAN)
        if human_wins:
            return -1000000, None
            
        ai_wins, _ = self.game_logic.check_win(Player.AI)
        if ai_wins:
            return 1000000, None
            
        if depth == 0 or self.game_logic.is_board_full():
            return self.score_position(Player.AI) - self.score_position(Player.HUMAN), None
        
        valid_moves = self.get_adjacent_moves()
        
        # Limit number of positions to evaluate for performance
        if len(valid_moves) > GameConfig.AI.MAX_SEARCH_POSITIONS:
            # Sort moves by potential and take top N
            valid_moves.sort(key=lambda move: self._move_potential(move, Player.AI if maximizing else Player.HUMAN), 
                            reverse=maximizing)
            valid_moves = valid_moves[:GameConfig.AI.MAX_SEARCH_POSITIONS]
        
        if maximizing:  # AI's turn
            max_eval = float('-inf')
            best_move = None
            
            for move in valid_moves:
                row, col = move
                board[row][col] = Player.AI.value
                
                eval_score, _ = self.minimax(depth-1, alpha, beta, False)
                board[row][col] = Player.EMPTY.value
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                    # Early exit if we find a winning move
                    if eval_score == 1000000:
                        break
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            
            return max_eval, best_move
        
        else:  # Human's turn
            min_eval = float('inf')
            best_move = None
            
            for move in valid_moves:
                row, col = move
                board[row][col] = Player.HUMAN.value
                
                eval_score, _ = self.minimax(depth-1, alpha, beta, True)
                board[row][col] = Player.EMPTY.value
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                    # Early exit if we find a losing move
                    if eval_score == -1000000:
                        break
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            
            return min_eval, best_move
    
    def _move_potential(self, move: Tuple[int, int], player: Player) -> int:
        row, col = move
        board = self.game_logic.board
        original = board[row][col]
        board[row][col] = player.value
        
        score = 0
        for direction in Direction:
            if direction == Direction.HORIZONTAL:
                start_col = max(0, col - GameConfig.WIN_LENGTH + 1)
                end_col = min(GameConfig.BOARD_SIZE - GameConfig.WIN_LENGTH, col)
                for c in range(start_col, end_col + 1):
                    window = [board[row][c+i] for i in range(GameConfig.WIN_LENGTH)]
                    score += self.evaluate_window(window, player)
        
        board[row][col] = original
        return score