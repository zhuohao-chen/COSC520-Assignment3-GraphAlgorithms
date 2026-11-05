import unittest
from graph.graph import Graph
from algorithms.graph_coloring import greedy_basic_coloring, largest_degree_first_coloring


class TestColoring(unittest.TestCase):
    def setUp(self):
        self.graph = Graph({1: {2, 3}, 2: {1, 3}, 3: {1, 2}, 4: set()})

    def assert_valid_coloring(self, coloring):
        self.assertEqual(set(coloring), self.graph.vertices)
        for edge in self.graph.edges:
            u, v = tuple(edge)
            self.assertNotEqual(coloring[u], coloring[v])

    def test_basic(self):
        self.assert_valid_coloring(greedy_basic_coloring(self.graph))

    def test_degree_ordering(self):
        self.assert_valid_coloring(largest_degree_first_coloring(self.graph))

    def test_empty_graph(self):
        self.assertEqual(greedy_basic_coloring(Graph({})), {})
        self.assertEqual(largest_degree_first_coloring(Graph({})), {})


if __name__ == '__main__':
    unittest.main()
