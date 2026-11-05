# COSC 520 — Assignment 3 Code Framework

Python 3.10+ recommended. Algorithms are intentionally **NOT implemented**:
replace `NotImplementedError` in the four algorithm functions with your own implementations.

## Setup

```bash
python -m pip install -r requirements.txt
```

## Test

```bash
python -m unittest discover -s tests -v
```

Tests for unfinished algorithms will fail until implemented. This is expected.

## Demo

```bash
python main.py
```

## Input format

`graph.dataset_loader.load_edge_list` accepts one `u v` undirected edge per line, integer node IDs. It does not preserve isolated vertices in an edge-list file. DIMACS `.col` and BHOSLIB parsing are TODOs.

## Benchmark

After algorithms are implemented:

```python
from benchmarks.benchmark import benchmark
benchmark('datasets/example.txt', trials=5)
```

## Suggested experiments

- Compare runtime and solution size for the two Vertex Cover methods.
- Compare runtime and number of colors for the two Graph Coloring methods.
- Use multiple graph sizes and repeat randomized trials with recorded seeds.
- Inspect solution validity before reporting measurements.

## Academic integrity

The framework was AI-assisted. Complete the algorithms yourself, verify all code, and disclose assistance in your report according to the assignment instructions.
