"""Read a basic whitespace-separated edge list (one 'u v' edge per line)."""
from pathlib import Path
from graph.graph import Graph
from typing import Union


def load_edge_list(path: Union[str, Path]) -> Graph:
    """Load an undirected graph from a plain edge-list file.

    Input: path to a text file; lines with '#' prefix are ignored.
    Output: Graph with integer node IDs.
    Note: BHOSLIB/FRB DIMACS files need a separate parser (TODO).
    """
    adjacency: dict[int, set[int]] = {}
    with open(path, encoding='utf-8') as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            values = line.split()
            if len(values) != 2:
                raise ValueError(f'Line {line_number}: expected two node IDs')
            u, v = map(int, values)
            if u == v:
                raise ValueError(f'Line {line_number}: self-loop')
            adjacency.setdefault(u, set()).add(v)
            adjacency.setdefault(v, set()).add(u)
    return Graph(adjacency)



def load_dimacs_col(path: Union[str, Path]) -> Graph:
    """
    Load an undirected graph in ASCII DIMACS format.

    Input: Path to a .col, .mis, or .clq file.
    Output: A Graph containing all vertices and edges.
    """
    adjacency = {}
    declared_vertices = None
    declared_edges = None
    edge_count = 0

    with open(path, encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()

            if not line or line.startswith("c"):
                continue

            parts = line.split()

            if parts[0] == "p":
                if len(parts) != 4 or parts[1] != "edge":
                    raise ValueError("Invalid DIMACS header")

                declared_vertices = int(parts[2])
                declared_edges = int(parts[3])

                # Include isolated vertices as well.
                adjacency = {
                    i: set()
                    for i in range(1, declared_vertices + 1)
                }

            elif parts[0] == "e":
                if declared_vertices is None:
                    raise ValueError("Missing DIMACS header")

                if len(parts) != 3:
                    raise ValueError(
                        f"Invalid edge at line {line_number}"
                    )

                u = int(parts[1])
                v = int(parts[2])

                if not (1 <= u <= declared_vertices and
                        1 <= v <= declared_vertices):
                    raise ValueError("Vertex ID out of range")

                if u == v:
                    raise ValueError("Self-loop detected")

                if v in adjacency[u]:
                    raise ValueError("Duplicate edge detected")

                adjacency[u].add(v)
                adjacency[v].add(u)
                edge_count += 1

            else:
                raise ValueError(
                    f"Unknown DIMACS line at {line_number}"
                )

    if declared_vertices is None:
        raise ValueError("DIMACS header not found")

    if edge_count != declared_edges:
        raise ValueError(
            f"Expected {declared_edges} edges, "
            f"but found {edge_count}"
        )

    return Graph(adjacency)

