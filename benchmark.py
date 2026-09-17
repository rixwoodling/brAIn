#!/usr/bin/env python3

import time

from database import Database
from memories import Memories


# Benchmark a function and return elapsed milliseconds.
def benchmark(function, *args):
    start = time.perf_counter()
    result = function(*args)
    elapsed = (time.perf_counter() - start) * 1000

    return result, elapsed


# Create test memories.
def create_test_memories(memories):
    test_data = [
        ("benchmark_name", "Rix"),
        ("benchmark_color", "Red"),
        ("benchmark_food", "Sushi"),
        ("benchmark_job", "Linux Engineer"),
        ("benchmark_os", "Linux"),
    ]

    results = []

    for key, value in test_data:
        _, elapsed = benchmark(memories.remember, key, value)
        results.append(elapsed)

    return results


# Benchmark memory search.
def benchmark_search(memories):
    _, elapsed = benchmark(
        memories.search,
        "benchmark_color"
    )

    return elapsed


# Benchmark memory recall by key.
def benchmark_recall(memories):
    _, elapsed = benchmark(
        memories.recall,
        "benchmark_color"
    )

    return elapsed


# Remove benchmark memories.
def cleanup(memories):
    for key in [
        "benchmark_name",
        "benchmark_color",
        "benchmark_food",
        "benchmark_job",
        "benchmark_os",
    ]:
        memories.forget(key)


# Run the benchmark pipeline.
def run_pipeline():
    db = Database()
    memories = Memories(db)

    write_times = create_test_memories(memories)
    search_time = benchmark_search(memories)
    recall_time = benchmark_recall(memories)

    print("brAIn Benchmark")
    print("────────────────────────────")
    print(f"Memories written:   {len(write_times)}")
    print(
        f"Write average:      "
        f"{sum(write_times) / len(write_times):.3f} ms"
    )
    print(f"Search:             {search_time:.3f} ms")
    print(f"Recall:             {recall_time:.3f} ms")

    cleanup(memories)
    db.close()


# Run the benchmark.
def main():
    run_pipeline()


if __name__ == "__main__":
    main()
