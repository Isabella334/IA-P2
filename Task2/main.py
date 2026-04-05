import time
from alpha_beta import AlphaBetaAgent
from evaluator import HeuristicEvaluator
from minimax import MinimaxAgent
from network import Network
from game import GameState

MAX_DEPTH = 4
DEFENSE_START_NODE = 0
ATTACKER_START_NODE = 19

def main():
    network = Network(num_nodes=20, edge_probability=0.35, seed=42)

    initial_state = GameState(
        network        = network,
        defense_nodes  = {DEFENSE_START_NODE},
        attacker_nodes = {ATTACKER_START_NODE},
        turn           = "MAX"
    )

    print("Sección 1 - Eval(s) numeric example")

    evaluator = HeuristicEvaluator()

    defense_frontier  = initial_state.available_moves("MAX")
    attacker_frontier = initial_state.available_moves("MIN")

    defense_accumulated_value  = network.value_of(DEFENSE_START_NODE)
    attacker_accumulated_value = network.value_of(ATTACKER_START_NODE)

    defense_frontier_value  = sum(network.value_of(n) for n in defense_frontier)
    attacker_frontier_value = sum(network.value_of(n) for n in attacker_frontier)

    defense_available_moves  = len(defense_frontier)
    attacker_available_moves = len(attacker_frontier)

    eval_result = evaluator.evaluate(initial_state)

    print(f"Formula: Eval(s) = (V_def - V_att) + 0.5*(F_def - F_att) + 0.3*(C_def - C_att)")
    print(f"Defense  holds node {DEFENSE_START_NODE}  -> accumulated value = {defense_accumulated_value}")
    print(f"Attacker holds node {ATTACKER_START_NODE} -> accumulated value = {attacker_accumulated_value}")
    print(f"Defense  frontier nodes = {sorted(defense_frontier)}")
    print(f"Attacker frontier nodes = {sorted(attacker_frontier)}")
    print(f"Defense  frontier value (F_def) = {defense_frontier_value}")
    print(f"Attacker frontier value (F_att) = {attacker_frontier_value}")
    print(f"Defense  available moves (C_def) = {defense_available_moves}")
    print(f"Attacker available moves (C_att) = {attacker_available_moves}")
    print(f"Eval = ({defense_accumulated_value}-{attacker_accumulated_value}) + 0.5*({defense_frontier_value}-{attacker_frontier_value}) + 0.3*({defense_available_moves}-{attacker_available_moves})")
    print(f"Eval = {eval_result:.2f}")

    print("\nSección 2 - Comparación Minimax puro vs Poda Alpha-Beta")

    minimax_agent    = MinimaxAgent(max_depth=MAX_DEPTH)
    alphabeta_agent  = AlphaBetaAgent(max_depth=MAX_DEPTH)

    start = time.time()
    minimax_value, minimax_move = minimax_agent.choose_move(initial_state)
    minimax_time = time.time() - start

    start = time.time()
    alphabeta_value, alphabeta_move = alphabeta_agent.choose_move(initial_state)
    alphabeta_time = time.time() - start

    minimax_nodes_expanded  = minimax_agent.nodes_expanded
    alphabeta_nodes_expanded = alphabeta_agent.nodes_expanded
    nodes_reduction  = (1 - alphabeta_nodes_expanded / minimax_nodes_expanded) * 100
    speedup          = minimax_time / alphabeta_time if alphabeta_time > 0 else float("inf")
    same_decision    = minimax_move == alphabeta_move and round(minimax_value, 6) == round(alphabeta_value, 6)

    print(f"{'Metric':<32} {'Minimax':>14} {'Alpha-Beta':>14}")
    print(f"{'Chosen move':<32} {'node ' + str(minimax_move):>14} {'node ' + str(alphabeta_move):>14}")
    print(f"{'Evaluation value':<32} {minimax_value:>14.2f} {alphabeta_value:>14.2f}")
    print(f"{'Nodes expanded':<32} {minimax_nodes_expanded:>14,} {alphabeta_nodes_expanded:>14,}")
    print(f"{'Time (s)':<32} {minimax_time:>14.6f} {alphabeta_time:>14.6f}")
    print(f"Nodes reduction : {nodes_reduction:.1f}%")
    print(f"Speedup         : {speedup:.2f}x")
    print(f"Same decision   : {'YES - pruning is correct' if same_decision else 'NO - check implementation'}")

    print("\nSección 3 - Simulación completa")

    current_state       = GameState(
        network        = network,
        defense_nodes  = {DEFENSE_START_NODE},
        attacker_nodes = {ATTACKER_START_NODE},
        turn           = "MAX"
    )
    game_agent          = AlphaBetaAgent(max_depth=MAX_DEPTH)
    total_nodes_in_game = 0

    while not current_state.is_terminal():
        print(current_state)

        turn_value, chosen_move = game_agent.choose_move(current_state)
        total_nodes_in_game += game_agent.nodes_expanded

        if chosen_move is not None:
            print(f"{current_state.turn} captures node {chosen_move} (value={network.value_of(chosen_move)}, eval={turn_value:.2f}, expanded={game_agent.nodes_expanded})")
            current_state = current_state.apply_move(chosen_move, current_state.turn)
        else:
            current_state = current_state.skip_turn()

    defense_score  = current_state.score_defense()
    attacker_score = current_state.score_attacker()

    print(f"Game over at turn {current_state.turn_count}")
    print(f"Defense  (MAX) : nodes={sorted(current_state.defense_nodes)}")
    print(f"Attacker (MIN) : nodes={sorted(current_state.attacker_nodes)}")
    print(f"Score  DEF={defense_score}  ATK={attacker_score}")

    if defense_score > attacker_score:
        print("DEFENSE WINS")
    elif attacker_score > defense_score:
        print("ATTACKER WINS")
    else:
        print("DRAW")

    print(f"Total nodes expanded in game : {total_nodes_in_game:,}")


if __name__ == "__main__":
    main()
