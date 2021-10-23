from typing import List
import numpy as np
import networkx as nx
from Functions.Algorithms.cycles import find_positive_cycles
from Functions.Algorithms.factorizations import get_factorizations


# Relevant functions


def highlight_positive_cycles(igraph: nx.classes.digraph.DiGraph) -> None:
    positive_cycles = find_positive_cycles(igraph)
    for cycle in positive_cycles:
        draw_one_cycle(igraph, cycle, "green", "green", "green")


def highlight_factorizations(igraph: nx.classes.digraph.DiGraph, marker_sets: List[List[str]]) -> None:
    factorizations = get_factorizations(marker_sets)
    for f in factorizations:
        colors = get_colors(len(f))
        for i, equivalent_marker_set in enumerate(f):
            mark_markers(igraph, equivalent_marker_set, colors[i])

# Help functions


def draw_one_cycle(igraph, cycle: List[str], pos_color: str, neg_color: str, both_color: str) -> None:
    for index in range(len(cycle)):
        if len(igraph.adj[cycle[index]][cycle[np.mod(index + 1, len(cycle))]]["sign"]) == 1:
            if 1 in igraph.adj[cycle[index]][cycle[np.mod(index + 1, len(cycle))]]["sign"]:
                igraph.adj[cycle[index]][cycle[np.mod(index + 1, len(cycle))]]["color"] = pos_color
            else:
                igraph.adj[cycle[index]][cycle[np.mod(index + 1, len(cycle))]]["color"] = neg_color
        else:
            igraph.adj[cycle[index]][cycle[np.mod(index + 1, len(cycle))]]["color"] = both_color


def mark_markers(igraph, markers: List[str], color: str = "green", style: str = "interior") -> None:
    if style == "interior":
        for m in markers:
            igraph.nodes[m]["fillcolor"] = color
    elif style == "margin":
        for m in markers:
            igraph.nodes[m]["color"] = color
    else:
        raise Exception


def get_colors(count: int) -> List[str]:
    color_list = [
        "aqua",
        "greenyellow",
        "gold",
        "deeppink",
        "mediumpurple",
        "coral",
        "lime",
        "indianred",
        "lightslategray",
        "lightslategrey",
        "lightsteelblue",
        "lightyellow",
        "lime",
    ]
    chosen_colors = color_list[:count]
    return chosen_colors
