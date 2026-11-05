
"""Demonstrate the four implemented graph algorithms."""

import random

from graph.graph import Graph
from algorithms.vertex_cover import basic_vertex_cover, randomized_vertex_cover
from algorithms.graph_coloring import greedy_basic_coloring, largest_degree_first_coloring


def main():
    graph = Graph({
        "A": {"B", "C"},
        "B": {"A", "C"},
        "C": {"A", "B"}
    })

    basic_cover = basic_vertex_cover(graph)
    random_cover = randomized_vertex_cover(graph, random.Random(42))
    basic_coloring = greedy_basic_coloring(graph)
    degree_coloring = largest_degree_first_coloring(graph)

    print("=== Vertex Cover ===")
    print("Basic:", basic_cover, "Size:", len(basic_cover))
    print("Randomized:", random_cover, "Size:", len(random_cover))

    print("\n=== Graph Coloring ===")
    print("Basic Greedy:", basic_coloring)
    print("Largest Degree First:", degree_coloring)


if __name__ == "__main__":
    main()
