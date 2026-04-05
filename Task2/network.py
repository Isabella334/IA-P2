import random
from collections import defaultdict

class Network:
    def __init__(self, num_nodes=20, edge_probability=0.35, seed=63):
        random.seed(seed)
        self.num_nodes = num_nodes
        self.adjacency = self.generate(edge_probability)
        self.node_values = {
            node: random.randint(1, 20) for node in range(num_nodes)
        }

    def generate(self, edge_probability):
        adjacency = defaultdict(set)
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                if random.random() < edge_probability:
                    adjacency[i].add(j)
                    adjacency[j].add(i)
        for i in range(self.num_nodes - 1):
            if not adjacency[i]:
                adjacency[i].add(i + 1)
                adjacency[i + 1].add(i)
        return adjacency

    def neighbors(self, node):
        return self.adjacency[node]

    def all_nodes(self):
        return set(range(self.num_nodes))

    def value_of(self, node):
        return self.node_values[node]

    def __repr__(self):
        lines = [f"Red de servidores con: {self.num_nodes} nodos"]
        for node in range(self.num_nodes):
            lines.append(f"  Nodo {node:2d} (val={self.node_values[node]:2d}) -> {sorted(self.adjacency[node])}")
        return "\n".join(lines)
