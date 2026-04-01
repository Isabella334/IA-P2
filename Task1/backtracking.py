import time

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A'],
    'D': ['B']
}

domains = {
    node: ['Rojo', 'Verde', 'Azul', 'Amarillo']
    for node in graph
}

steps_puro = 0
steps_opt = 0

def is_consistent(var, value, assignment):
    for neighbor in graph[var]:
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    return True

# BACKTRACKING PURO

def backtrack_puro(assignment):
    global steps_puro
    steps_puro += 1

    if len(assignment) == len(graph):
        return assignment

    for var in graph:
        if var not in assignment:
            break

    for value in domains[var]:
        if is_consistent(var, value, assignment):
            assignment[var] = value

            result = backtrack_puro(assignment)
            if result:
                return result

            del assignment[var]

    return None

# FORWARD CHECKING

def forward_checking(var, value, domains, graph):
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

# MCV

def select_unassigned_variable(assignment, domains):
    unassigned = [v for v in domains if v not in assignment]
    return min(unassigned, key=lambda var: len(domains[var]))

# BACKTRACKING OPTIMIZADO

def backtrack_opt(assignment, domains, graph):
    global steps_opt
    steps_opt += 1

    if len(assignment) == len(graph):
        return assignment

    var = select_unassigned_variable(assignment, domains)

    for value in domains[var]:
        if is_consistent(var, value, assignment):
            assignment[var] = value

            success, removed = forward_checking(var, value, domains, graph)

            if success:
                result = backtrack_opt(assignment, domains, graph)
                if result:
                    return result

            del assignment[var]
            restore_domains(domains, removed)

    return None

# Análisis

# ---- Backtracking puro ----
steps_puro = 0
start = time.time()

solution_puro = backtrack_puro({})

end = time.time()
time_puro = end - start

# ---- Backtracking optimizado ----
steps_opt = 0
domains_copy = {var: list(values) for var, values in domains.items()}

start = time.time()

solution_opt = backtrack_opt({}, domains_copy, graph)

end = time.time()
time_opt = end - start

print("Backtracking puro:")
print("Solución:", solution_puro)
print("Pasos:", steps_puro)
print("Tiempo:", time_puro)

print("\nBacktracking optimizado (FC + MCV):")
print("Solución:", solution_opt)
print("Pasos:", steps_opt)
print("Tiempo:", time_opt)
