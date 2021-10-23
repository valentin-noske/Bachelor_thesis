import networkx as nx
import numpy as np
from typing import List

# Relevant functions


def find_cycles(igraph: nx.classes.digraph.DiGraph) -> List[List[str]]:
    edges = list(igraph.edges())
    g = nx.DiGraph(edges)
    cycles = list(nx.algorithms.cycles.simple_cycles(g))
    return cycles


def find_positive_cycles(igraph: nx.classes.digraph.DiGraph) -> List[List[str]]:
    positive_cycles = []
    cycles = find_cycles(igraph)
    for i, cycle in enumerate(cycles):
        sign = 1
        for index in range(len(cycle)):
            signs_of_edge = list(igraph.adj[cycle[index]][cycle[np.mod(index + 1, len(cycle))]]["sign"])
            if len(signs_of_edge) == 1:
                sign = sign * signs_of_edge[0]
            else:
                sign = 1
                break
        if sign > 0:
            positive_cycles.append(cycle)
    return positive_cycles
