import random
from Task2.game import GameState
from Task2.network import Network

P_SUCCESS = 0.80
P_FAIL = 0.20

def simulate_game(
    network: Network,
    defense_agent,
    attacker_agent,
    defense_start: int = 0,
    attacker_start: int = 19,
    stochastic: bool = True,
    rng_seed: int | None = None,
    verbose: bool = False,
) -> dict:
    rng = random.Random(rng_seed)

    state = GameState(
        network = network,
        defense_nodes = {defense_start},
        attacker_nodes = {attacker_start},
        turn = "MAX",
    )

    turns_played = 0
    failed_actions = 0

    while not state.is_terminal():
        current_player = state.turn

        if current_player == "MAX":
            _, move = defense_agent.choose_move(state)
        else:
            _, move = attacker_agent.choose_move(state)

        if move is None:
            state = state.skip_turn()
        else:
            if stochastic and rng.random() < P_FAIL:
                failed_actions += 1
                if verbose:
                    print(f"  Turno {state.turn_count:2d} | {current_player} intenta nodo {move} -> FALLA")
                state = state.skip_turn()
            else:
                if verbose:
                    print(f"  Turno {state.turn_count:2d} | {current_player} captura  nodo {move} "
                          f"(val={network.value_of(move)})")
                state = state.apply_move(move, current_player)

        turns_played += 1

    result = {
        "def_score": state.score_defense(),
        "att_score": state.score_attacker(),
        "winner": ("MAX" if state.score_defense() > state.score_attacker()
                          else "MIN" if state.score_attacker() > state.score_defense()
                          else "DRAW"),
        "turns": state.turn_count,
        "failed_actions": failed_actions,
        "def_nodes": sorted(state.defense_nodes),
        "att_nodes": sorted(state.attacker_nodes),
    }
    return result