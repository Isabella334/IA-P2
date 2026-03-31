# Grafo
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A'],
    'D': ['B']
}

# Dominios (protocolos)
domains = {
    node: ['Rojo', 'Verde', 'Azul', 'Amarillo']
    for node in graph
}
domains_copy = {var: list(values) for var, values in domains.items()}

steps = 0

def is_consistent(var, value, assignment):
    for neighbor in graph[var]:
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    return True

# Algoritmo de backtracking search
def backtrack(assignment, domains, graph):
    global steps
    steps += 1
    if len(assignment) == len(graph):
        return assignment
        
    for var in graph:
        if var not in assignment:
            break

    for value in domains[var]:
        if is_consistent(var, value, assignment):
            assignment[var] = value
            
            # Forward checking
            success, removed = forward_checking(var, value, domains, graph)
            if success:
                result = backtrack(assignment, domains, graph)
                if result:
                    return result
            del assignment[var]
            restore_domains(domains, removed)
    return None

#Forward checking
def forward_checking(var, value, domains, graph):
    removed = []

    for neighbor in graph[var]:
        if neighbor in domains and value in domains[neighbor]:
            domains[neighbor].remove(value)
            removed.append((neighbor, value))

            # Si un dominio queda vacío → fallo
            if len(domains[neighbor]) == 0:
                return False, removed

    return True, removed

def restore_domains(domains, removed):
    for var, value in removed:
        domains[var].append(value)

#MCV 
def select_unassigned_variable(assignment, domains):
    unassigned = [v for v in domains if v not in assignment]
    
    # Escoge la variable con menor tamaño de dominio
    return min(unassigned, key=lambda var: len(domains[var]))


solution = backtrack({}, domains_copy, graph)

print("Solución encontrada:")
print(solution)
print("Pasos:", steps)


