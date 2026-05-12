"""
Benchmark script for the REPORT — Evaluation section (25 points).

What is measured:
1. DFS maze generation: runtime vs maze size
2. BFS pathfinding: runtime, nodes explored, and path length vs maze size

Both algorithms are tested across a range of maze sizes, with multiple trials
per size to produce reliable averages. Results are printed to the terminal and
saved as CSV files for use in report charts (e.g. Excel or Google Sheets).

Run with: python evaluation.py
"""

import time
import statistics
import csv

from maze_generator import generate_maze, get_all_path_cells
from pathfinding import bfs_with_stats


def benchmark_maze_generation(sizes, trials_per_size=10):
    """Measure DFS maze generation runtime across a range of maze sizes."""
    print("\n=== DFS Maze Generation Benchmark ===")
    print(f"{'Size':>10} {'Cells':>8} {'Avg(ms)':>10} {'Stdev(ms)':>10}")
    results = []
    for size in sizes:
        times = []
        for trial in range(trials_per_size):
            t0 = time.perf_counter()
            grid = generate_maze(rows=size, cols=size, seed=trial)
            t1 = time.perf_counter()
            times.append((t1 - t0) * 1000)  # convert to milliseconds
        avg = statistics.mean(times)
        std = statistics.stdev(times) if len(times) > 1 else 0.0
        cells = size * size
        print(f"{size:>10} {cells:>8} {avg:>10.3f} {std:>10.3f}")
        results.append({"size": size, "cells": cells,
                        "avg_ms": avg, "stdev_ms": std})
    return results


def benchmark_bfs_pathfinding(sizes, trials_per_size=20):
    """Measure BFS pathfinding (worst-case: top-left corner to bottom-right corner)."""
    print("\n=== BFS Pathfinding Benchmark (corner to corner) ===")
    print(f"{'Size':>6} {'Path Len':>10} {'Explored':>10} "
          f"{'Avg(ms)':>10} {'Stdev(ms)':>10}")
    results = []
    for size in sizes:
        times = []
        path_lengths = []
        explored_counts = []
        for trial in range(trials_per_size):
            grid = generate_maze(rows=size, cols=size, seed=trial)
            # Corner-to-corner is the worst-case path in a square maze
            start = (1, 1)
            goal = (size - 2, size - 2)
            stats = bfs_with_stats(grid, start, goal)
            times.append(stats["runtime_seconds"] * 1000)
            path_lengths.append(stats["path_length"])
            explored_counts.append(stats["nodes_explored"])
        avg_time = statistics.mean(times)
        std_time = statistics.stdev(times) if len(times) > 1 else 0.0
        avg_path = statistics.mean(path_lengths)
        avg_explored = statistics.mean(explored_counts)
        print(f"{size:>6} {avg_path:>10.1f} {avg_explored:>10.1f} "
              f"{avg_time:>10.3f} {std_time:>10.3f}")
        results.append({
            "size": size,
            "avg_path_length": avg_path,
            "avg_nodes_explored": avg_explored,
            "avg_runtime_ms": avg_time,
            "stdev_runtime_ms": std_time,
        })
    return results


def save_csv(rows, path):
    if not rows:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved: {path}")


def main():
    sizes = [11, 21, 31, 41, 51, 71, 101]

    print("Running DAA Pac-Man algorithm benchmarks...")
    print("(This may take a few seconds for larger maze sizes)\n")

    maze_results = benchmark_maze_generation(sizes, trials_per_size=10)
    bfs_results = benchmark_bfs_pathfinding(sizes, trials_per_size=20)

    save_csv(maze_results, "results_maze_generation.csv")
    save_csv(bfs_results, "results_bfs_pathfinding.csv")

    print("\nDone. Import the CSV files into Excel or Google Sheets to plot charts for the report.")


if __name__ == "__main__":
    main()
