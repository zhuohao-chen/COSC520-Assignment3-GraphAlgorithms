# COSC 520 — Assignment 3: Vertex Cover and Graph Coloring

This project implements and compares four graph algorithms for COSC 520 Assignment 3 at the University of British Columbia Okanagan.

The objective is to evaluate the computational performance and solution quality of different approaches to the Vertex Cover and Graph Coloring problems.

## Implemented Algorithms

**Vertex Cover**
- Basic Vertex Cover: Selects an arbitrary edge and adds both endpoints to the cover.
- Randomized Vertex Cover: Selects an edge and randomly adds one of its endpoints to the cover.

**Graph Coloring**
- Basic Greedy Coloring: Assigns the smallest available color to each vertex in its original insertion order.
- Largest Degree First (LDF): Sorts vertices by descending degree before applying greedy coloring.

All four algorithms are implemented in Python without using existing graph algorithm libraries.

## Setup

Python 3.9 or later is required.

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Unit Tests

Run all unit tests:

```bash
python -m unittest discover -s tests -v
```

The tests verify the validity of Vertex Cover and Graph Coloring solutions, including empty graphs.

## Demo

Run the example:

```bash
python main.py
```

## Datasets

The project supports two graph input formats:

- **Edge List:** Plain text files containing one undirected edge `u v` per line.
- **DIMACS:** `.mis`, `.clq`, and `.col` files using the DIMACS graph format.

The experiments use the [BHOSLIB benchmark datasets](https://rb-bench.github.io/benchmarks/hidden-opt-graph.html), including four FRB groups:

| Dataset | Vertices | Instances |
|---|---:|---:|
| FRB30-15 | 450 | 5 |
| FRB35-17 | 595 | 5 |
| FRB40-19 | 760 | 5 |
| FRB45-21 | 945 | 5 |

MIS graphs are used for Vertex Cover comparisons, while the complementary CLQ graphs are used for Graph Coloring comparisons.

The benchmark datasets can be downloaded from the official BHOSLIB website and placed in the `datasets/` directory.

## Benchmark

Benchmarking is implemented in `benchmarks/benchmark.py` using Python's `time.perf_counter()`.

Each graph instance is evaluated using 10 trials per algorithm. The benchmark records execution time, solution size, and solution validity. Raw measurements and summary statistics are saved as CSV files.

Example — Vertex Cover dataset:

```bash
python -c "from benchmarks.benchmark import benchmark; benchmark('datasets/frb30-15-mis', trials=10, output='results/frb30_15_mis.csv')"
```

Example — Graph Coloring dataset:

```bash
python -c "from benchmarks.benchmark import benchmark; benchmark('datasets/frb30-15-clq', trials=10, output='results/frb30_15_clq.csv')"
```

The benchmark runs all four algorithms on each input graph. Only the relevant algorithm pairs are used for the main MIS and CLQ comparisons.

## Visualization

The visualization script `benchmarks/plot_results.py` reads the benchmark summary CSV files and generates four figures:

1. Vertex Cover — Runtime
2. Vertex Cover — Solution Size
3. Graph Coloring — Runtime
4. Graph Coloring — Number of Colors

Generate the figures using:

```bash
python -m benchmarks.plot_results
```

The figures are saved in `results/figures/`.

Error bars represent the standard deviation across the five graph-instance means within each dataset group.

## Author

Zhuohao Chen  
University of British Columbia Okanagan  
COSC 520 — Assignment 3 (Fall 2026)