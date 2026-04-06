import time
import os
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

random.seed(7)
NUM_NODES = 18
nodes = [f"S{i}" for i in range(1, NUM_NODES + 1)]

graph = {node: [] for node in nodes}

shuffled = nodes[:]
random.shuffle(shuffled)
for i in range(1, len(shuffled)):
    u = shuffled[i]
    v = shuffled[random.randint(0, i - 1)]
    if v not in graph[u]:
        graph[u].append(v)
        graph[v].append(u)

extra_edges = 28
attempts = 0
while extra_edges > 0 and attempts < 50000:
    u = random.choice(nodes)
    v = random.choice(nodes)
    if u != v and v not in graph[u]:
        graph[u].append(v)
        graph[v].append(u)
        extra_edges -= 1
    attempts += 1

# Dominio: 4 protocolos
PROTOCOLS = ['Rojo', 'Verde', 'Azul', 'Amarillo']

def fresh_domains():
    return {node: list(PROTOCOLS) for node in nodes}

def is_consistent(var, value, assignment):
    for neighbor in graph[var]:
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    return True

def backtrack_puro(assignment, stats):
    stats['steps'] += 1

    if len(assignment) == len(nodes):
        return assignment

    # Selección de variable: primer nodo no asignado (orden fijo)
    var = next(v for v in nodes if v not in assignment)

    for value in PROTOCOLS:
        stats['intentos'] += 1
        if is_consistent(var, value, assignment):
            assignment[var] = value
            result = backtrack_puro(assignment, stats)
            if result:
                return result
            del assignment[var]
            stats['backtracks'] += 1

    return None

def forward_checking(var, value, domains):
    removed = []
    for neighbor in graph[var]:
        if value in domains[neighbor]:
            domains[neighbor].remove(value)
            removed.append((neighbor, value))
            if len(domains[neighbor]) == 0:
                return False, removed
    return True, removed

def restore_domains(domains, removed):
    for var, value in removed:
        domains[var].append(value)

def backtrack_fc(assignment, domains, stats):
    stats['steps'] += 1

    if len(assignment) == len(nodes):
        return assignment

    # Orden fijo (sin MRV)
    var = next(v for v in nodes if v not in assignment)

    for value in list(domains[var]):
        stats['intentos'] += 1
        if is_consistent(var, value, assignment):
            assignment[var] = value
            ok, removed = forward_checking(var, value, domains)
            if ok:
                result = backtrack_fc(assignment, domains, stats)
                if result:
                    return result
            del assignment[var]
            restore_domains(domains, removed)
            stats['backtracks'] += 1

    return None

# BT + FC + MRV

def select_mrv(assignment, domains):
    unassigned = [v for v in nodes if v not in assignment]
    # MRV: mínimo de valores restantes → más restringida
    return min(unassigned, key=lambda var: len(domains[var]))

def backtrack_fc_mrv(assignment, domains, stats):
    stats['steps'] += 1

    if len(assignment) == len(nodes):
        return assignment
    var = select_mrv(assignment, domains)

    for value in list(domains[var]):
        stats['intentos'] += 1
        if is_consistent(var, value, assignment):
            assignment[var] = value
            ok, removed = forward_checking(var, value, domains)
            if ok:
                result = backtrack_fc_mrv(assignment, domains, stats)
                if result:
                    return result
            del assignment[var]
            restore_domains(domains, removed)
            stats['backtracks'] += 1

    return None

# Backtracking puro
stats_puro = {'steps': 0, 'intentos': 0, 'backtracks': 0}
start = time.time()
sol_puro = backtrack_puro({}, stats_puro)
time_puro = time.time() - start

# BT + FC (sin MRV)
stats_fc = {'steps': 0, 'intentos': 0, 'backtracks': 0}
start = time.time()
sol_fc = backtrack_fc({}, fresh_domains(), stats_fc)
time_fc = time.time() - start

# BT + FC + MRV ---
stats_mrv = {'steps': 0, 'intentos': 0, 'backtracks': 0}
start = time.time()
sol_mrv = backtrack_fc_mrv({}, fresh_domains(), stats_mrv)
time_mrv = time.time() - start

print("=" * 50)
print("         RESULTADOS - TASK 1")
print("=" * 50)

for label, sol, stats, t in [
    ("Backtracking Puro",        sol_puro, stats_puro, time_puro),
    ("BT + Forward Checking",    sol_fc,   stats_fc,   time_fc),
    ("BT + FC + MRV",            sol_mrv,  stats_mrv,  time_mrv),
]:
    print(f"\n{label}")
    print(f"  Solución encontrada : {'Sí' if sol else 'No'}")
    print(f"  Llamadas recursivas : {stats['steps']}")
    print(f"  Asignaciones intent.: {stats['intentos']}")
    print(f"  Backtracks          : {stats['backtracks']}")
    print(f"  Tiempo              : {t:.6f} s")

COLOR_MAP = {
    'Rojo':     '#e74c3c',
    'Verde':    '#2ecc71',
    'Azul':     '#3498db',
    'Amarillo': '#f1c40f',
}

def build_nx_graph():
    G = nx.Graph()
    G.add_nodes_from(nodes)
    for node in nodes:
        for neighbor in graph[node]:
            if node < neighbor:
                G.add_edge(node, neighbor)
    return G

def get_node_colors(G, solution=None):
    if solution:
        return [COLOR_MAP[solution[n]] for n in G.nodes()]
    return ['#bdc3c7'] * len(G.nodes())

G = build_nx_graph()
pos = nx.spring_layout(G, seed=42, k=1.8)

fig, ax = plt.subplots(figsize=(10, 8))
ax.set_title("Red de Servidores — Sin Protocolo Asignado", fontsize=14, fontweight='bold', pad=15)
nx.draw_networkx(G, pos, ax=ax,
                 node_color='#bdc3c7', node_size=600,
                 font_size=8, font_color='#2c3e50',
                 edge_color='#95a5a6', width=1.5,
                 with_labels=True)
ax.axis('off')
plt.tight_layout()
plt.savefig("grafo_original.png", dpi=150, bbox_inches='tight')
plt.close()

fig, ax = plt.subplots(figsize=(10, 8))
ax.set_title("Red de Servidores — Protocolos Asignados (BT+FC+MRV)", fontsize=14, fontweight='bold', pad=15)
colors = get_node_colors(G, sol_mrv)
nx.draw_networkx(G, pos, ax=ax,
                 node_color=colors, node_size=600,
                 font_size=8, font_color='#2c3e50',
                 edge_color='#7f8c8d', width=1.5,
                 with_labels=True)

legend_patches = [mpatches.Patch(color=v, label=k) for k, v in COLOR_MAP.items()]
ax.legend(handles=legend_patches, loc='lower left', fontsize=10, title="Protocolo")
ax.axis('off')
plt.tight_layout()
plt.savefig("grafo_coloreado.png", dpi=150, bbox_inches='tight')
plt.close()

labels     = ['BT Puro', 'BT + FC', 'BT + FC + MRV']
pasos      = [stats_puro['steps'],    stats_fc['steps'],    stats_mrv['steps']]
intentos   = [stats_puro['intentos'], stats_fc['intentos'], stats_mrv['intentos']]
backtracks = [stats_puro['backtracks'], stats_fc['backtracks'], stats_mrv['backtracks']]
tiempos    = [time_puro, time_fc, time_mrv]

BAR_COLORS = ['#e74c3c', '#f39c12', '#2ecc71']
x = range(len(labels))

fig, axes = plt.subplots(2, 2, figsize=(13, 10))
fig.suptitle("Comparativa de Rendimiento — Backtracking CSP", fontsize=15, fontweight='bold')

def make_bar(ax, values, title, ylabel, log=False):
    bars = ax.bar(labels, values, color=BAR_COLORS, edgecolor='white', linewidth=1.2, width=0.5)
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=9)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.01,
                f'{val:,}' if isinstance(val, int) else f'{val:.5f}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    if log and max(values) > 0:
        ax.set_yscale('log')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='x', labelsize=9)

make_bar(axes[0, 0], pasos,      "Llamadas Recursivas (steps)",    "Cantidad",  log=True)
make_bar(axes[0, 1], intentos,   "Asignaciones Intentadas",        "Cantidad",  log=True)
make_bar(axes[1, 0], backtracks, "Número de Backtracks",           "Cantidad",  log=True)
make_bar(axes[1, 1], tiempos,    "Tiempo de Ejecución (s)",        "Segundos")

fig.subplots_adjust(top=0.92, hspace=0.35, wspace=0.3)
plt.savefig("comparativa_rendimiento.png", dpi=100)
plt.close()