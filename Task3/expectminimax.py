import math
from Task2.evaluator import HeuristicEvaluator
from Task2.game import GameState

P_SUCCESS = 0.80
P_FAIL = 0.20


class ExpectiminimaxAgent:

    def __init__(self, max_depth: int = 4):
        self.max_depth = max_depth
        self.evaluator = HeuristicEvaluator()
        self.nodes_expanded = 0

    def choose_move(self, state: GameState) -> tuple[float, int | None]:
        self.nodes_expanded = 0
        return self._expectiminimax(state, depth=0)

    def _expectiminimax(self, state: GameState, depth: int) -> tuple[float, int | None]:
        self.nodes_expanded += 1

        if state.is_terminal():
            return state.terminal_score(), None

        if depth == self.max_depth:
            return self.evaluator.evaluate(state), None

        moves = state.available_moves(state.turn)

        if not moves:
            value, _ = self._expectiminimax(state.skip_turn(), depth + 1)
            return value, None

        if state.turn == "MAX":
            return self._maximize(state, depth, moves)
        else:
            return self._minimize(state, depth, moves)

    def _maximize(self, state: GameState, depth: int, moves: list) -> tuple[float, int | None]:
        best_value = -math.inf
        best_move  = None

        for move in moves:
            expected = self._chance_node(state, move, "MAX", depth)
            if expected > best_value:
                best_value = expected
                best_move  = move

        return best_value, best_move

    def _minimize(self, state: GameState, depth: int, moves: list) -> tuple[float, int | None]:
        best_value = math.inf
        best_move  = None

        for move in moves:
            expected = self._chance_node(state, move, "MIN", depth)
            if expected < best_value:
                best_value = expected
                best_move  = move

        return best_value, best_move

    def _chance_node(self, state: GameState, move: int, player: str, depth: int) -> float:
        self.nodes_expanded += 1 

        success_state = state.apply_move(move, player)
        success_value, _ = self._expectiminimax(success_state, depth + 1)

        fail_state = state.skip_turn()
        fail_value, _ = self._expectiminimax(fail_state, depth + 1)

        return P_SUCCESS * success_value + P_FAIL * fail_value