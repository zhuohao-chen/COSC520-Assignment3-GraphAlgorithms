"""Plot COSC 520 Assignment 3 benchmark results from summary CSV files.

Reads the eight *_summary.csv files produced by benchmarks/benchmark.py and
creates four publication-ready figures. Run from any working directory:
    python -m benchmarks.plot_results
or:
    python benchmarks/plot_results.py

The error bars represent the sample standard deviation across the five graph
instances (using each instance's mean over trials), not the variation among
individual timing trials.
"""

import csv
import statistics
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Save plots without needing an interactive display.
import matplotlib.pyplot as plt


# This script is intended to live at <project>/benchmarks/plot_results.py.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"
OUTPUT_DIR = RESULTS_DIR / "figures"

DATASET_GROUPS = [
    ("frb30_15", 450),
    ("frb35_17", 595),
    ("frb40_19", 760),
    ("frb45_21", 945),
]


def read_grouped_results(kind, algorithms, metric):
    """Return per-algorithm x/mean/std values from summary files.

    kind: 'mis' or 'clq'.
    algorithms: algorithm identifiers in the benchmark CSV.
    metric: 'mean_seconds' or 'mean_solution_size'.
    """
    grouped = {algorithm: {"x": [], "mean": [], "std": []}
               for algorithm in algorithms}

    for dataset_name, expected_vertices in DATASET_GROUPS:
        csv_path = RESULTS_DIR / (dataset_name + "_" + kind + "_summary.csv")
        if not csv_path.is_file():
            raise FileNotFoundError(
                "Missing file: {}. Run benchmarks before plotting.".format(csv_path)
            )

        with csv_path.open("r", newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))

        for algorithm in algorithms:
            matching = [row for row in rows if row["algorithm"] == algorithm]
            if not matching:
                raise ValueError("No results for {} in {}".format(algorithm, csv_path))

            sizes = {int(row["vertices"]) for row in matching}
            if sizes != {expected_vertices}:
                raise ValueError(
                    "Unexpected vertex counts for {}: {}".format(csv_path, sizes)
                )

            # One row per graph instance. Each row is already averaged over trials.
            instance_means = [float(row[metric]) for row in matching]
            if metric == "mean_seconds":
                instance_means = [value * 1000 for value in instance_means]

            grouped[algorithm]["x"].append(expected_vertices)
            grouped[algorithm]["mean"].append(statistics.mean(instance_means))
            grouped[algorithm]["std"].append(
                statistics.stdev(instance_means) if len(instance_means) > 1 else 0.0
            )

            print("{} {} {}: mean={:.3f}, SD={:.3f}, instances={}".format(
                kind, dataset_name, algorithm,
                grouped[algorithm]["mean"][-1],
                grouped[algorithm]["std"][-1], len(instance_means)))

    return grouped


def plot_metric(kind, algorithms, labels, metric, ylabel, filename):
    """Create a line chart with one line per algorithm and instance-level SD bars."""
    data = read_grouped_results(kind, algorithms, metric)
    fig, ax = plt.subplots(figsize=(7.2, 4.5))

    for algorithm, label in zip(algorithms, labels):
        series = data[algorithm]
        ax.errorbar(
            series["x"], series["mean"], yerr=series["std"],
            fmt="-o", capsize=3, linewidth=1.8, markersize=5,
            label=label
        )

    ax.set_xlabel("Number of vertices")
    ax.set_ylabel(ylabel)
    ax.set_xticks([vertices for _, vertices in DATASET_GROUPS])
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / filename
    fig.savefig(str(output_path), dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Saved:", output_path)


def main():
    vc_algorithms = ["vertex_cover_basic", "vertex_cover_random"]
    vc_labels = ["Basic Vertex Cover", "Randomized Vertex Cover"]
    gc_algorithms = ["coloring_basic", "coloring_degree"]
    gc_labels = ["Basic Greedy", "Largest Degree First"]

    plot_metric("mis", vc_algorithms, vc_labels,
                "mean_seconds", "Runtime (ms)",
                "figure1_vertex_cover_runtime.png")
    plot_metric("mis", vc_algorithms, vc_labels,
                "mean_solution_size", "Vertex cover size",
                "figure2_vertex_cover_size.png")
    plot_metric("clq", gc_algorithms, gc_labels,
                "mean_seconds", "Runtime (ms)",
                "figure3_coloring_runtime.png")
    plot_metric("clq", gc_algorithms, gc_labels,
                "mean_solution_size", "Number of colors",
                "figure4_coloring_colors.png")


if __name__ == "__main__":
    main()
