"""Simple undirected graph represented by an adjacency dictionary."""
from dataclasses import dataclass
from typing import Dict, Set, Hashable

Node = Hashable


@dataclass
class Graph:
    adjacency: Dict[Node, Set[Node]]

    def __post_init__(self) -> None:
        # Make an independent copy; ensure every node appears in the dictionary.
        self.adjacency = {u: set(neighbors) for u, neighbors in self.adjacency.items()}
        for neighbors in list(self.adjacency.values()):
            for v in neighbors:
                self.adjacency.setdefault(v, set())
        for u, neighbors in self.adjacency.items():
            if u in neighbors:
                raise ValueError('Self-loops are not supported for this assignment.')
            for v in neighbors:
                if u not in self.adjacency[v]:
                    raise ValueError(f'Asymmetric adjacency: {u!r} - {v!r}')

    @property
    def vertices(self) -> set[Node]:
        return set(self.adjacency)

    @property
    def edges(self) -> set[frozenset[Node]]:
        return {frozenset((u, v)) for u, neighbors in self.adjacency.items() for v in neighbors}

    @property
    def num_vertices(self) -> int:
        return len(self.adjacency)

    @property
    def num_edges(self) -> int:
        return len(self.edges)
