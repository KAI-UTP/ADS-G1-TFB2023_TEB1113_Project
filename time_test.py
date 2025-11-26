import time
import random
from typing import List

from baseline import FCFSTriageSystem, Patient
from optimized import PriorityTriageSystem


def generate_patients(n: int) -> List[Patient]:
    patients: List[Patient] = []
    arrival_time = 0
    for i in range(1, n + 1):
        severity = random.randint(1, 5)
        name = f"Patient_{i}"
        arrival_time += 1
        patients.append(
            Patient(
                id=i,
                name=name,
                severity=severity,
                arrival_time=arrival_time,
            )
        )
    return patients


def compute_median_severity(patients: List[Patient]) -> float:
    if not patients:
        return 0.0

    severities = [p.severity for p in patients]
    severities.sort()

    n = len(severities)
    mid = n // 2

    if n % 2 == 1:
        return float(severities[mid])
    else:
        return (severities[mid - 1] + severities[mid]) / 2.0


def benchmark_system(system, patients: List[Patient]) -> float:
    start = time.perf_counter()

    for p in patients:
        system.arrive(p)

    while not system.is_empty():
        system.serve_next()

    end = time.perf_counter()
    return end - start


def main() -> None:
    random.seed(42)

    sizes = [1000, 5000, 10000, 20000]

    print("Benchmarking FCFS vs Priority Queue (heap)")
    print("------------------------------------------")

    for n in sizes:
        patients = generate_patients(n)
        median_sev = compute_median_severity(patients)

        baseline_system = FCFSTriageSystem()
        t_baseline = benchmark_system(baseline_system, patients)

        optimized_system = PriorityTriageSystem()
        t_optimized = benchmark_system(optimized_system, patients)

        print(f"Number of patients: {n:6d}")
        print(f"  Median severity in dataset: {median_sev:.2f}")
        print(f"  Baseline FCFS time:         {t_baseline:0.6f} seconds")
        print(f"  Priority Queue time:        {t_optimized:0.6f} seconds")
        print()


if __name__ == "__main__":
    main()

