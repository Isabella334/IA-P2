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

def is_consistent(var, value, assignment):
    for neighbor in graph[var]:
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    return True

# Algoritmo de backtracking search
def backtrack(assignment):
    if len(assignment) == len(graph):
        return assignment

    # Seleccionar variable no asignada
    for var in graph:
        if var not in assignment:
            break

    for value in domains[var]:
        if is_consistent(var, value, assignment):
            assignment[var] = value

            result = backtrack(assignment)
            if result:
                return result

            # Backtrack
            del assignment[var]

    return None

solution = backtrack({})

print("Solución encontrada:")
print(solution)
