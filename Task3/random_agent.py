import random
from Task2.game import GameState

class RandomAgent:
    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)

    def choose_move(self, state: GameState) -> tuple[None, int | None]:
        moves = state.available_moves(state.turn)
        if not moves:
            return None, None
        return None, self.rng.choice(moves)