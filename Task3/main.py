
from network import Network
from alpha_beta import AlphaBetaAgent
from expectiminimax import ExpectiminimaxAgent
from random_agent import RandomAgent
from simulator import simulate_game

MAX_DEPTH = 4
SIM_DEPTH = 3
DEFENSE_START = 0
ATTACKER_START = 19
N_GAMES = 15
NETWORK_SEED = 63


def comparativa_agentes(network: Network):
    print("Análisis Comparativo")
    print(f"Número de partidas por experimento : {N_GAMES}")
    print("El oponente siempre es un agente aleatorio\n")

    minimax_agent = AlphaBetaAgent(max_depth=SIM_DEPTH)
    expecti_agent = ExpectiminimaxAgent(max_depth=SIM_DEPTH)

    print("Minimax puro (Alpha-Beta) vs Agente Aleatorio (mundo estocástico)")
    _run_experiment(
        network        = network,
        defense_agent  = minimax_agent,
        label_defense  = "Minimax(AB)",
        n_games        = N_GAMES,
        stochastic     = True,
    )

    print("Expectiminimax vs Agente Aleatorio (mundo estocástico)")
    _run_experiment(
        network        = network,
        defense_agent  = expecti_agent,
        label_defense  = "Expectiminimax",
        n_games        = N_GAMES,
        stochastic     = True,
    )


def _run_experiment(network, defense_agent, label_defense, n_games, stochastic):
    wins, draws, losses = 0, 0, 0
    total_def_score, total_att_score = 0, 0
    total_failed, total_turns = 0, 0
    margin_list = []

    for i in range(n_games):
        att_agent = RandomAgent(seed=i * 7 + 13)
        result = simulate_game(
            network        = network,
            defense_agent  = defense_agent,
            attacker_agent = att_agent,
            defense_start  = DEFENSE_START,
            attacker_start = ATTACKER_START,
            stochastic     = stochastic,
            rng_seed       = i * 31 + 5,
            verbose        = False,
        )
        if result["winner"] == "MAX":
            wins += 1
        elif result["winner"] == "DRAW":
            draws += 1
        else:
            losses += 1

        margin = result["def_score"] - result["att_score"]
        margin_list.append(margin)
        total_def_score += result["def_score"]
        total_att_score += result["att_score"]
        total_failed    += result["failed_actions"]
        total_turns     += result["turns"]

    avg_margin  = sum(margin_list) / n_games
    avg_failed  = total_failed / n_games
    avg_turns   = total_turns / n_games

    print(f"  Agente defensa : {label_defense}")
    print(f"  Partidas       : {n_games}  (entorno {'estocástico' if stochastic else 'determinista'})")
    print(f"  Victorias MAX  : {wins}  ({wins/n_games*100:.1f}%)")
    print(f"  Empates        : {draws}")
    print(f"  Derrotas MAX   : {losses}  ({losses/n_games*100:.1f}%)")
    print(f"  Margen promedio (DEF - ATK) : {avg_margin:+.1f}")
    print(f"  Acciones fallidas promedio  : {avg_failed:.1f} / partida")
    print(f"  Turnos promedio             : {avg_turns:.1f}")
    print()

    return {
        "label":      label_defense,
        "wins":       wins,
        "draws":      draws,
        "losses":     losses,
        "avg_margin": avg_margin,
        "avg_failed": avg_failed,
        "avg_turns":  avg_turns,
        "n":          n_games,
    }

def main():
    print("Task 3: Expectiminimax y Análisis Comparativo\n")

    network = Network(num_nodes=20, edge_probability=0.35, seed=NETWORK_SEED)
    print(f"Red: {network.num_nodes} nodos, semilla={NETWORK_SEED}")
    print()

    comparativa_agentes(network)


if __name__ == "__main__":
    main()