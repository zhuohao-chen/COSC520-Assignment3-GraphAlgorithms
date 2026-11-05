"""Vertex cover algorithms. Implement both algorithms yourself."""
import random
from graph.graph import Graph, Node
from typing import Optional


def basic_vertex_cover(graph: Graph) -> set[Node]:
    """Return a cover: repeatedly select an edge and add BOTH endpoints.

    Input: undirected graph.
    Output: a set of selected vertices covering every edge.
    """
    cover = set()
    remaining_edges = set(graph.edges)
    while remaining_edges:
        u, v = next(iter(remaining_edges))
        cover.add(u)
        cover.add(v)

        new_edge = set()
        for a, b in remaining_edges:
            if u not in (a, b) and v not in (a, b):
                new_edge.add((a,b))

        remaining_edges = new_edge

    return cover

def randomized_vertex_cover(
    graph: Graph,
    rng: Optional[random.Random] = None
) -> set[Node]:
    """Return a valid cover by choosing one random endpoint of a selected edge.

    Input: graph, optional seeded random generator.
    Output: a set of vertices covering every edge.
    """

    if rng is None:
        rng = random.Random()

    cover = set()
    remaining_edges = set(graph.edges)
    while remaining_edges:
        u, v = rng.choice(list(remaining_edges))
        chosen_vertex = rng.choice([u, v])
        cover.add(chosen_vertex)

        new_edge = set()
        for a, b in remaining_edges:
            if chosen_vertex not in (a, b):
                new_edge.add((a,b))

        remaining_edges = new_edge

    return cover
