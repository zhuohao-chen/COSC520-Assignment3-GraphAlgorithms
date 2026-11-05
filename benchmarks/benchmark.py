
"""Benchmark vertex cover and graph coloring algorithms."""

import csv
import random
import statistics
from pathlib import Path
from time import perf_counter

from algorithms.vertex_cover import basic_vertex_cover, randomized_vertex_cover
from algorithms.graph_coloring import greedy_basic_coloring, largest_degree_first_coloring
from graph.dataset_loader import load_edge_list, load_dimacs_col


def validate_vertex_cover(graph, cover):
    """Return True if every edge has at least one endpoint in cover."""
    return all(any(node in cover for node in edge) for edge in graph.edges)


def validate_coloring(graph, coloring):
    """Return True if every vertex is colored and adjacent colors differ."""
    if set(coloring) != graph.vertices:
        return False

    if not all(isinstance(c, int) and c >= 0 for c in coloring.values()):
        return False

    return all(
        coloring[u] != coloring[v]
        for u, v in (tuple(edge) for edge in graph.edges)
    )


def load_graph(path):
    """Load a graph according to its file extension."""
    if path.suffix.lower() in (".mis", ".clq", ".col"):
        return load_dimacs_col(path)
    return load_edge_list(path)


def benchmark(path, trials=10, output="results/timings.csv"):
    """
    Benchmark all four algorithms on one file or a directory.

    Input: dataset path, number of trials, CSV output path.
    Output: detailed CSV results and a summary CSV.
    """
    dataset_path = Path(path)

    if trials < 1:
        raise ValueError("trials must be at least 1")

    if dataset_path.is_dir():
        files = sorted(
            p for p in dataset_path.iterdir()
            if p.is_file() and p.suffix.lower()
            in (".mis", ".clq", ".col", ".txt")
        )
    elif dataset_path.is_file():
        files = [dataset_path]
    else:
        raise FileNotFoundError(dataset_path)

    if not files:
        raise ValueError("No supported graph files found")

    rows = []

    for file_path in files:
        graph = load_graph(file_path)

        print(
            f"Testing {file_path.name} "
            f"({graph.num_vertices} vertices, "
            f"{graph.num_edges} edges)"
        )

        algorithms = [
            ("vertex_cover_basic",
             lambda seed: basic_vertex_cover(graph)),
            ("vertex_cover_random",
             lambda seed: randomized_vertex_cover(
                 graph, random.Random(seed))),
            ("coloring_basic",
             lambda seed: greedy_basic_coloring(graph)),
            ("coloring_degree",
             lambda seed: largest_degree_first_coloring(graph)),
        ]

        for algorithm_name, run in algorithms:
            for trial in range(trials):

                # Time only the algorithm.
                start = perf_counter()
                result = run(trial)
                elapsed = perf_counter() - start

                # Validate after timing.
                if algorithm_name.startswith("vertex_cover"):
                    valid = validate_vertex_cover(graph, result)
                    solution_size = len(result)
                else:
                    valid = validate_coloring(graph, result)
                    solution_size = len(set(result.values()))

                if not valid:
                    raise ValueError(
                        f"Invalid result: {file_path.name}, "
                        f"{algorithm_name}, trial {trial}"
                    )

                rows.append({
                    "dataset": file_path.name,
                    "algorithm": algorithm_name,
                    "trial": trial,
                    "vertices": graph.num_vertices,
                    "edges": graph.num_edges,
                    "seconds": elapsed,
                    "solution_size": solution_size,
                    "valid": valid
                })

            print(f"  {algorithm_name}: {trials} trials completed")

    # Save detailed results.
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    # Aggregate statistics for each dataset and algorithm.
    groups = {}

    for row in rows:
        key = (row["dataset"], row["algorithm"])
        groups.setdefault(key, []).append(row)

    summary = []

    for (dataset, algorithm), group in groups.items():
        times = [r["seconds"] for r in group]
        sizes = [r["solution_size"] for r in group]

        summary.append({
            "dataset": dataset,
            "algorithm": algorithm,
            "vertices": group[0]["vertices"],
            "edges": group[0]["edges"],
            "trials": len(group),
            "mean_seconds": statistics.mean(times),
            "std_seconds": statistics.stdev(times)
                           if len(times) > 1 else 0,
            "mean_solution_size": statistics.mean(sizes),
            "std_solution_size": statistics.stdev(sizes)
                                 if len(sizes) > 1 else 0
        })

    summary_path = output_path.with_name(
        output_path.stem + "_summary.csv"
    )

    with summary_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)

    print(f"\nSaved {len(rows)} rows to {output_path}")
    print(f"Saved {len(summary)} summary rows to {summary_path}")
