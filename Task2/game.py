from network import Network

class GameState:
    MAX_TURNS = 30

    def __init__(self, network: Network, defense_nodes: set, attacker_nodes: set, turn: str, turn_count: int = 0):
        self.network = network
        self.defense_nodes = set(defense_nodes)
        self.attacker_nodes = set(attacker_nodes)
        self.turn = turn
        self.turn_count = turn_count

    def available_moves(self, player: str) -> list:
        owned = self.defense_nodes if player == "MAX" else self.attacker_nodes
        captured = self.defense_nodes or self.attacker_nodes

        moves = set()
        for node in owned:
            for neighbor in self.network.neighbors(node):
                if neighbor not in captured:
                    moves.add(neighbor)

        return list(moves)

    def apply_move(self, move: int, player: str) -> "GameState":
        new_defense = set(self.defense_nodes)
        new_attacker = set(self.attacker_nodes)

        if player == "MAX":
            new_defense.add(move)
        else:
            new_attacker.add(move)
        next_turn = "MIN" if player == "MAX" else "MAX"

        return GameState(self.network, new_defense, new_attacker, next_turn, self.turn_count + 1)

    def skip_turn(self) -> "GameState":
        next_turn = "MIN" if self.turn == "MAX" else "MAX"
        return GameState(self.network, self.defense_nodes, self.attacker_nodes, next_turn, self.turn_count + 1)

    def is_terminal(self) -> bool:
        all_captured = (self.defense_nodes | self.attacker_nodes) == self.network.all_nodes()
        no_moves_max = len(self.available_moves("MAX")) == 0
        no_moves_min = len(self.available_moves("MIN")) == 0
        turn_limit = self.turn_count >= self.MAX_TURNS
        return all_captured or (no_moves_max and no_moves_min) or turn_limit

    def terminal_score(self) -> float:
        score_defense = sum(self.network.value_of(n) for n in self.defense_nodes)
        score_attacker = sum(self.network.value_of(n) for n in self.attacker_nodes)
        return score_defense - score_attacker

    def score_defense(self) -> int:
        return sum(self.network.value_of(n) for n in self.defense_nodes)

    def score_attacker(self) -> int:
        return sum(self.network.value_of(n) for n in self.attacker_nodes)

    def __repr__(self):
        return (
            f"Turno {self.turn_count:2d} | Jugador: {self.turn} | "
            f"DEF={sorted(self.defense_nodes)} | ATK={sorted(self.attacker_nodes)}"
        )
