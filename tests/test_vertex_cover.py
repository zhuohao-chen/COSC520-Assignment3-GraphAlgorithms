"""Run: python -m unittest discover -s tests -v"""
import random
import unittest
from graph.graph import Graph
from algorithms.vertex_cover import basic_vertex_cover, randomized_vertex_cover


class TestVertexCover(unittest.TestCase):
    def setUp(self):
        self.graph = Graph({1: {2, 3}, 2: {1, 3}, 3: {1, 2}, 4: set()})

    def assert_valid_cover(self, cover):
        self.assertTrue(cover <= self.graph.vertices)
        for edge in self.graph.edges:
            self.assertTrue(bool(cover.intersection(edge)), f'Uncovered edge: {edge}')

    def test_basic_cover(self):
        self.assert_valid_cover(basic_vertex_cover(self.graph))

    def test_randomized_cover(self):
        for seed in range(5):
            self.assert_valid_cover(randomized_vertex_cover(self.graph, random.Random(seed)))

    def test_empty_graph(self):
        graph = Graph({})
        self.assertEqual(basic_vertex_cover(graph), set())
        self.assertEqual(randomized_vertex_cover(graph, random.Random(0)), set())


if __name__ == '__main__':
    unittest.main()
