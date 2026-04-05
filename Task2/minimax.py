import math
from evaluator import HeuristicEvaluator
from game import GameState

class MinimaxAgent:
    def __init__(self, max_depth: int = 4):
        self.max_depth = max_depth
        self.evaluator = HeuristicEvaluator()
        self.nodes_expanded = 0
 
    def choose_move(self, state: GameState) -> tuple[float, int | None]:
        self.nodes_expanded = 0
        return self.minimax(state, depth=0)
 
    def minimax(self, state: GameState, depth: int) -> tuple[float, int | None]:
        self.nodes_expanded += 1
 
        if state.is_terminal():
            return state.terminal_score(), None
 
        if depth == self.max_depth:
            return self.evaluator.evaluate(state), None
 
        moves = state.available_moves(state.turn)
 
        if not moves:
            value, _ = self.minimax(state.skip_turn(), depth + 1)
            return value, None
 
        if state.turn == "MAX":
            return self.maximize(state, depth, moves)
        else:
            return self.minimize(state, depth, moves)
 
    def maximize(self, state, depth, moves):
        best_value = -math.inf
        best_move  = None
        for move in moves:
            child_value, _ = self.minimax(state.apply_move(move, "MAX"), depth + 1)
            if child_value > best_value:
                best_value = child_value
                best_move  = move
        return best_value, best_move
 
    def minimize(self, state, depth, moves):
        best_value = math.inf
        best_move  = None
        for move in moves:
            child_value, _ = self.minimax(state.apply_move(move, "MIN"), depth + 1)
            if child_value < best_value:
                best_value = child_value
                best_move  = move
        return best_value, best_move
 
