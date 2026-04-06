import math
from evaluator import HeuristicEvaluator
from game import GameState

class AlphaBetaAgent:
    def __init__(self, max_depth: int = 4):
        self.max_depth = max_depth
        self.evaluator = HeuristicEvaluator()
        self.nodes_expanded = 0
 
    def choose_move(self, state: GameState) -> tuple[float, int | None]:
        self.nodes_expanded = 0
        return self.alphabeta(state, depth=0, alpha=-math.inf, beta=math.inf)
 
    def alphabeta(self, state: GameState, depth: int, alpha: float, beta: float) -> tuple[float, int | None]:
        self.nodes_expanded += 1
 
        if state.is_terminal():
            return state.terminal_score(), None
 
        if depth == self.max_depth:
            return self.evaluator.evaluate(state), None
 
        moves = state.available_moves(state.turn)
 
        if not moves:
            value, _ = self.alphabeta(state.skip_turn(), depth + 1, alpha, beta)
            return value, None
 
        if state.turn == "MAX":
            return self.maximize(state, depth, moves, alpha, beta)
        else:
            return self.minimize(state, depth, moves, alpha, beta)
 
    def maximize(self, state, depth, moves, alpha, beta):
        best_value = -math.inf
        best_move  = None
        for move in moves:
            child_value, _ = self.alphabeta(state.apply_move(move, "MAX"), depth + 1, alpha, beta)
            if child_value > best_value:
                best_value = child_value
                best_move  = move
            alpha = max(alpha, best_value)
            if alpha >= beta:
                break
        return best_value, best_move
 
    def minimize(self, state, depth, moves, alpha, beta):
        best_value = math.inf
        best_move  = None
        for move in moves:
            child_value, _ = self.alphabeta(state.apply_move(move, "MIN"), depth + 1, alpha, beta)
            if child_value < best_value:
                best_value = child_value
                best_move  = move
            beta = min(beta, best_value)
            if alpha >= beta:
                break
        return best_value, best_move
