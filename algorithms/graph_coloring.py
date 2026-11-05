from graph.graph import Graph, Node


def greedy_basic_coloring(graph: Graph) -> dict[Node, int]:
    """Color vertices in a fixed, documented order, with smallest legal color.

    Input: undirected graph.
    Output: mapping node -> nonnegative integer color.
    """
    coloring = {}
    
    for node in graph.adjacency:
        used_colors = set()
        for neighbor in graph.adjacency[node]:
            if neighbor in coloring:
                used_colors.add(coloring[neighbor])
        color = 0
        while color in used_colors:
            color += 1
        coloring[node] = color
    return coloring


def largest_degree_first_coloring(graph: Graph) -> dict[Node, int]:
    """Color vertices by descending degree, with smallest legal color.

    Input: undirected graph.
    Output: mapping node -> nonnegative integer color.
    """
    ordered_nodes = sorted(
        graph.adjacency,
        key=lambda node: len(graph.adjacency[node]),
        reverse=True
    )
    coloring = {}
    for node in ordered_nodes:
        used_colors = set()
        for neighbor in graph.adjacency[node]:
            if neighbor in coloring:
                used_colors.add(coloring[neighbor])
        color = 0
        while color in used_colors:
            color += 1
        coloring[node] = color
    return coloring
