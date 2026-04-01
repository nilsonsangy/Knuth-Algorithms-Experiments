from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Tuple


@dataclass
class Metrics:
    comparisons: int = 0
    local_assignments: int = 0
    vector_assignments: int = 0

    def add(self, other: "Metrics") -> None:
        self.comparisons += other.comparisons
        self.local_assignments += other.local_assignments
        self.vector_assignments += other.vector_assignments


@dataclass
class PhaseResult:
    comparisons: int
    local_assignments: int
    vector_assignments: int
    time_seconds: float


@dataclass
class ExperimentRow:
    n: int
    permutations: int
    transitions: int
    offline: PhaseResult
    online: PhaseResult
    total: PhaseResult


def swap_adjacent(vec: List[int], i: int, metrics: Metrics) -> None:
    a = vec[i]
    b = vec[i + 1]
    metrics.local_assignments += 2

    vec[i] = b
    vec[i + 1] = a
    metrics.vector_assignments += 2


def algorithm_t_offline(n: int) -> Tuple[List[int], Metrics]:
    metrics = Metrics()

    perm = list(range(1, n + 1))
    dirs = [-1] * (n + 1)
    metrics.local_assignments += 2
    metrics.vector_assignments += n + (n + 1)

    total = math.factorial(n)
    metrics.local_assignments += 1

    transitions: List[int] = []
    metrics.local_assignments += 1

    for _ in range(total - 1):
        largest_mobile_value = -1
        largest_mobile_index = -1
        metrics.local_assignments += 2

        i = 0
        metrics.local_assignments += 1
        while True:
            metrics.comparisons += 1
            if i >= n:
                break

            value = perm[i]
            direction = dirs[value]
            neighbor_index = i + direction
            metrics.local_assignments += 3

            metrics.comparisons += 1
            left_ok = neighbor_index >= 0
            metrics.local_assignments += 1
            metrics.comparisons += 1
            right_ok = neighbor_index < n
            metrics.local_assignments += 1
            metrics.comparisons += 1
            if left_ok and right_ok:
                metrics.comparisons += 1
                if value > perm[neighbor_index]:
                    metrics.comparisons += 1
                    if value > largest_mobile_value:
                        largest_mobile_value = value
                        largest_mobile_index = i
                        metrics.local_assignments += 2

            i += 1
            metrics.local_assignments += 1

        metrics.comparisons += 1
        if largest_mobile_index == -1:
            break

        value = perm[largest_mobile_index]
        direction = dirs[value]
        neighbor_index = largest_mobile_index + direction
        metrics.local_assignments += 3

        transition_index = min(largest_mobile_index, neighbor_index)
        transitions.append(transition_index)
        metrics.local_assignments += 1
        metrics.vector_assignments += 1

        perm[largest_mobile_index], perm[neighbor_index] = perm[neighbor_index], perm[largest_mobile_index]
        metrics.vector_assignments += 2

        j = 1
        metrics.local_assignments += 1
        while True:
            metrics.comparisons += 1
            if j > n:
                break
            metrics.comparisons += 1
            if j > value:
                dirs[j] = -dirs[j]
                metrics.vector_assignments += 1
            j += 1
            metrics.local_assignments += 1

    return transitions, metrics


def algorithm_t_online(n: int, transitions: List[int], keep_permutations: bool) -> Tuple[List[List[int]], Metrics]:
    metrics = Metrics()

    perm = list(range(1, n + 1))
    metrics.local_assignments += 1
    metrics.vector_assignments += n

    permutations: List[List[int]] = [perm.copy()] if keep_permutations else []
    metrics.local_assignments += 1
    if keep_permutations:
        metrics.comparisons += 1
        metrics.vector_assignments += n
    else:
        metrics.comparisons += 1

    i = 0
    metrics.local_assignments += 1
    while True:
        metrics.comparisons += 1
        if i >= len(transitions):
            break

        swap_index = transitions[i]
        metrics.local_assignments += 1

        swap_adjacent(perm, swap_index, metrics)

        metrics.comparisons += 1
        if keep_permutations:
            permutations.append(perm.copy())
            metrics.vector_assignments += n

        i += 1
        metrics.local_assignments += 1

    return permutations, metrics


def phase_result(metrics: Metrics, elapsed: float) -> PhaseResult:
    return PhaseResult(
        comparisons=metrics.comparisons,
        local_assignments=metrics.local_assignments,
        vector_assignments=metrics.vector_assignments,
        time_seconds=elapsed,
    )


def run_range(start_n: int, end_n: int, sample_n: int) -> dict:
    rows: List[ExperimentRow] = []
    sample = {}

    n = start_n
    while n <= end_n:
        start = time.perf_counter()
        transitions, offline_metrics = algorithm_t_offline(n)
        offline_time = time.perf_counter() - start

        start = time.perf_counter()
        keep = n == sample_n
        permutations, online_metrics = algorithm_t_online(n, transitions, keep_permutations=keep)
        online_time = time.perf_counter() - start

        total_metrics = Metrics()
        total_metrics.add(offline_metrics)
        total_metrics.add(online_metrics)

        row = ExperimentRow(
            n=n,
            permutations=math.factorial(n),
            transitions=len(transitions),
            offline=phase_result(offline_metrics, offline_time),
            online=phase_result(online_metrics, online_time),
            total=phase_result(total_metrics, offline_time + online_time),
        )
        rows.append(row)

        if keep:
            sample = {
                "n": n,
                "first_permutations": permutations[: min(24, len(permutations))],
            }

        n += 1

    return {
        "algorithm": "T (Plain Changes Transitions)",
        "range": {"start": start_n, "end": end_n},
        "rows": [asdict(r) for r in rows],
        "sample": sample,
    }


def save_results(data: dict, output_path: Path) -> None:
    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def save_results_js(data: dict, output_path: Path) -> None:
    js_payload = "window.__ALGO_T_RESULTS__ = " + json.dumps(data, indent=2) + ";\n"
    output_path.write_text(js_payload, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="T algorithm with separate Offline/Online phase measurements.")
    parser.add_argument("--start", type=int, default=3, help="start n value (default: 3)")
    parser.add_argument("--end", type=int, default=10, help="end n value (default: 10)")
    parser.add_argument("--sample", type=int, default=5, help="sample n used in the visual demo (default: 5)")
    parser.add_argument("--output", type=Path, default=Path("results.json"), help="output JSON file")
    args = parser.parse_args()

    if args.start < 1 or args.end < args.start:
        raise ValueError("Invalid n range.")

    data = run_range(args.start, args.end, args.sample)
    save_results(data, args.output)

    js_output = args.output.with_suffix(".js")
    save_results_js(data, js_output)

    print(f"Results saved to: {args.output}")
    print(f"JavaScript results saved to: {js_output}")


if __name__ == "__main__":
    main()
