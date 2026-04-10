from __future__ import annotations

import math
import time
from dataclasses import dataclass, asdict
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
class AlgorithmTResult:
    offline: PhaseResult
    online: PhaseResult
    total: PhaseResult


@dataclass
class AlgorithmPResult:
    total: PhaseResult


@dataclass
class ExperimentRow:
    n: int
    t: AlgorithmTResult
    p: AlgorithmPResult
    p_improved: AlgorithmPResult
    break_even_runs_time_p: int | None
    break_even_runs_time_p_improved: int | None


REFERENCE_P_METRICS = {
    3: {"comparisons": 12, "local_assignments": 58, "vector_assignments": 24, "time_seconds": 2.30e-05},
    4: {"comparisons": 27, "local_assignments": 192, "vector_assignments": 97, "time_seconds": 1.00e-05},
    5: {"comparisons": 87, "local_assignments": 866, "vector_assignments": 482, "time_seconds": 4.60e-05},
    6: {"comparisons": 387, "local_assignments": 4948, "vector_assignments": 2883, "time_seconds": 0.000245},
    7: {"comparisons": 2187, "local_assignments": 33750, "vector_assignments": 20164, "time_seconds": 0.003576},
    8: {"comparisons": 14787, "local_assignments": 265592, "vector_assignments": 161285, "time_seconds": 0.015439},
    9: {"comparisons": 115587, "local_assignments": 2362234, "vector_assignments": 1451526, "time_seconds": 0.159122},
    10: {"comparisons": 1022787, "local_assignments": 23409276, "vector_assignments": 14515207, "time_seconds": 2.37966},
}

REFERENCE_P_IMPROVED_METRICS = {
    3: {"comparisons": 69, "local_assignments": 44, "vector_assignments": 23, "time_seconds": 1.70e-05},
    4: {"comparisons": 380, "local_assignments": 214, "vector_assignments": 96, "time_seconds": 3.70e-05},
    5: {"comparisons": 2395, "local_assignments": 1230, "vector_assignments": 481, "time_seconds": 0.000211},
    6: {"comparisons": 17274, "local_assignments": 8320, "vector_assignments": 2882, "time_seconds": 0.001083},
    7: {"comparisons": 141113, "local_assignments": 64502, "vector_assignments": 20163, "time_seconds": 0.0102},
    8: {"comparisons": 1290232, "local_assignments": 566188, "vector_assignments": 161284, "time_seconds": 0.076943},
    9: {"comparisons": 13063671, "local_assignments": 5530936, "vector_assignments": 1451525, "time_seconds": 0.75922},
    10: {"comparisons": 145151990, "local_assignments": 59667532, "vector_assignments": 14515206, "time_seconds": 8.5759},
}


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

    swap_plan: List[int] = []
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

        swap_index = min(largest_mobile_index, neighbor_index)
        swap_plan.append(swap_index)
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

    return swap_plan, metrics


def algorithm_t_online(n: int, swap_plan: List[int], keep_permutations: bool) -> Tuple[List[List[int]], Metrics]:
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
        if i >= len(swap_plan):
            break

        swap_index = swap_plan[i]
        metrics.local_assignments += 1

        swap_adjacent(perm, swap_index, metrics)

        metrics.comparisons += 1
        if keep_permutations:
            permutations.append(perm.copy())
            metrics.vector_assignments += n

        i += 1
        metrics.local_assignments += 1

    return permutations, metrics


def reference_phase_result(n: int, variant: str) -> PhaseResult:
    if variant == "improved":
        source = REFERENCE_P_IMPROVED_METRICS
    elif variant == "plain":
        source = REFERENCE_P_METRICS
    else:
        raise ValueError(f"Invalid P variant: {variant}")
    if n not in source:
        raise ValueError(f"No reference P metrics available for n={n}.")
    row = source[n]
    return PhaseResult(
        comparisons=row["comparisons"],
        local_assignments=row["local_assignments"],
        vector_assignments=row["vector_assignments"],
        time_seconds=row["time_seconds"],
    )


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
        swap_plan, offline_metrics = algorithm_t_offline(n)
        offline_time = time.perf_counter() - start

        start = time.perf_counter()
        keep = n == sample_n
        permutations, online_metrics = algorithm_t_online(n, swap_plan, keep_permutations=keep)
        online_time = time.perf_counter() - start

        p_total = reference_phase_result(n, variant="plain")
        p_improved_total = reference_phase_result(n, variant="improved")

        total_metrics = Metrics()
        total_metrics.add(offline_metrics)
        total_metrics.add(online_metrics)

        t_offline = phase_result(offline_metrics, offline_time)
        t_online = phase_result(online_metrics, online_time)
        t_total = phase_result(total_metrics, offline_time + online_time)
        denom_p = p_total.time_seconds - online_time
        break_even_runs_time_p = None
        if denom_p > 0:
            break_even_runs_time_p = max(1, math.ceil(offline_time / denom_p))

        denom_p_improved = p_improved_total.time_seconds - online_time
        break_even_runs_time_p_improved = None
        if denom_p_improved > 0:
            break_even_runs_time_p_improved = max(1, math.ceil(offline_time / denom_p_improved))

        row = ExperimentRow(
            n=n,
            t=AlgorithmTResult(offline=t_offline, online=t_online, total=t_total),
            p=AlgorithmPResult(total=p_total),
            p_improved=AlgorithmPResult(total=p_improved_total),
            break_even_runs_time_p=break_even_runs_time_p,
            break_even_runs_time_p_improved=break_even_runs_time_p_improved,
        )
        rows.append(row)

        if keep:
            sample = {
                "n": n,
                "first_permutations": permutations[: min(24, len(permutations))],
            }

        n += 1

    return {
        "algorithm": "T (Plain Changes)",
        "p_reference_source": "User-provided table image (P and Improved P)",
        "p_reference_variant": "P and Improved P",
        "range": {"start": start_n, "end": end_n},
        "rows": [asdict(r) for r in rows],
        "sample": sample,
    }