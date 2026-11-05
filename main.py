"""Demo entry point. Complete algorithm TODOs before running."""
from graph.graph import Graph
from algorithms.vertex_cover import basic_vertex_cover, randomized_vertex_cover
from algorithms.graph_coloring import greedy_basic_coloring, largest_degree_first_coloring


def main():
    graph = Graph({
        "A": {"B", "C"},
        "B": {"A", "C"},
        "C": {"A", "B"}
    })

    cover = basic_vertex_cover(graph)

    basic_vertex_cover(graph)
    randomized_vertex_cover(graph)
    greedy_basic_coloring(graph)
    largest_degree_first_coloring(graph)


if __name__ == '__main__':
    main()
