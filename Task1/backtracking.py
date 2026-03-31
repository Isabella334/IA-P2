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
