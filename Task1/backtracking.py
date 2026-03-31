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
