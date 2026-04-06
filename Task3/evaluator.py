from game import GameState

class HeuristicEvaluator:
    def __init__(self, frontier_weight = 0.5, mobility_weight  = 0.3) -> None:
        self.frontier_weight = frontier_weight
        self.mobility_weight = mobility_weight
 
    def evaluate(self, state: GameState) -> float:
        current_value   = state.terminal_score()
 
        frontier_max    = state.available_moves("MAX")
        frontier_min    = state.available_moves("MIN")
 
        frontier_value  = (sum(state.network.value_of(n) for n in frontier_max) - sum(state.network.value_of(n) for n in frontier_min))
        mobility_value  = len(frontier_max) - len(frontier_min)
 
        return (current_value + self.frontier_weight * frontier_value + self.mobility_weight * mobility_value)
