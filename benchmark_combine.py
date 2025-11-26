import time
import subprocess
import sys
import random
from typing import Tuple, Union

def generate_baseline_input(num_patients: int, seed: int = 42, measure_phase: str = "both") -> str:
    """
    Generate automated input for baseline.py (FIFO Queue).
    
    measure_phase: "enqueue" - only add patients
                   "dequeue" - only serve patients (requires pre-added patients)
                   "both" - add then serve all
    """
    random.seed(seed)
    queue_capacity = num_patients + 10
    
    input_lines = [str(queue_capacity)]
    
    if measure_phase in ["enqueue", "both"]:
        # Add all patients
        for i in range(num_patients):
            severity = random.randint(1, 5)
            input_lines.append("1")  # Add patient option
            input_lines.append(f"P{i+1}")  # Name
            input_lines.append(str(1000 + i))  # ID
            input_lines.append(str(severity))  # Severity
    
    if measure_phase in ["dequeue", "both"]:
        # Serve all patients
        for _ in range(num_patients):
            input_lines.append("2")  # Serve next option
    
    input_lines.append("9")  # Exit
    
    return "\n".join(input_lines) + "\n"

def generate_optimized_input(num_patients: int, seed: int = 42, measure_phase: str = "both") -> str:
    """
    Generate automated input for optimized.py (Heap Priority Queue).
    
    measure_phase: "enqueue" - setup and add patients
                   "dequeue" - setup and serve patients (requires pre-added patients)
                   "both" - setup, add then serve all
    """
    random.seed(seed)
    
    input_lines = ["2", "Dr1", "Dr2", str(min(num_patients + 10, 100))]
    
    if measure_phase in ["enqueue", "both"]:
        # Add all patients
        for i in range(num_patients):
            severity = random.randint(1, 5)
            input_lines.append("1")  # Add patient option
            input_lines.append(f"P{i+1}")  # Name
            input_lines.append(str(1000 + i))  # ID
            input_lines.append(str(severity))  # Severity
    
    if measure_phase in ["dequeue", "both"]:
        # Serve all patients
        for _ in range(num_patients):
            input_lines.append("3")  # Serve next option
    
    input_lines.append("11")  # Exit
    
    return "\n".join(input_lines) + "\n"

def run_benchmark(script_name: str, input_data: str, num_patients: int) -> Tuple[float, bool, str]:
    """
    Run benchmark and return execution time, success status, and error message.
    """
    try:
        start_time = time.perf_counter()
        
        result = subprocess.run(
            [sys.executable, script_name],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        
        success = result.returncode == 0
        error_msg = result.stderr if result.stderr else ""
        return elapsed_time, success, error_msg
        
    except subprocess.TimeoutExpired:
        return 120.0, False, "TIMEOUT"
    except Exception as e:
        return None, False, str(e)

def main():
    """
    Benchmark both baseline.py and optimized.py with completely separate enqueue/dequeue
    """
    patient_counts = [10, 50, 100, 500, 1000]
    baseline_enqueue = {}
    baseline_dequeue = {}
    optimized_enqueue = {}
    optimized_dequeue = {}
    
    # ========== ENQUEUE ONLY TESTS ==========
    print("=" * 90)
    print("ENQUEUE OPERATIONS - ADD ALL PATIENTS")
    print("=" * 90)
    print("\nTest Configuration:")
    print("- Operation: Only ENQUEUE (Add patients to queue)")
    print("- Patient Severity: Random 1-5 (5 = critical)")
    print("- Random Seed: 42 (reproducible)")
    print("- Patient Counts: 10, 50, 100, 500, 1000")
    print("=" * 90)
    
    print("\n" + "[BASELINE - FIFO QUEUE ENQUEUE]".center(90, "-"))
    print("-" * 90)
    
    for count in patient_counts:
        print(f"Enqueue {count:4d} patients...", end=" ", flush=True)
        input_data = generate_baseline_input(count, measure_phase="enqueue")
        elapsed_time, success, error_msg = run_benchmark("baseline.py", input_data, count)
        
        if success and elapsed_time is not None:
            baseline_enqueue[count] = elapsed_time
            print(f"[OK] {elapsed_time:.4f}s ({elapsed_time*1000:.2f}ms)")
        else:
            baseline_enqueue[count] = None
            print(f"[FAILED]")
    
    print("\n" + "[OPTIMIZED - PRIORITY QUEUE ENQUEUE]".center(90, "-"))
    print("-" * 90)
    
    for count in patient_counts:
        print(f"Enqueue {count:4d} patients...", end=" ", flush=True)
        input_data = generate_optimized_input(count, measure_phase="enqueue")
        elapsed_time, success, error_msg = run_benchmark("optimized.py", input_data, count)
        
        if success and elapsed_time is not None:
            optimized_enqueue[count] = elapsed_time
            print(f"[OK] {elapsed_time:.4f}s ({elapsed_time*1000:.2f}ms)")
        else:
            optimized_enqueue[count] = None
            print(f"[FAILED]")
    
    # Results table - ENQUEUE
    print("\n" + "=" * 90)
    print("ENQUEUE RESULTS SUMMARY")
    print("=" * 90)
    print(f"{'Patients':<12} | {'Baseline (s)':<16} | {'Optimized (s)':<16} | {'Speedup':<12}")
    print("-" * 65)
    
    for count in patient_counts:
        baseline_time = baseline_enqueue[count]
        optimized_time = optimized_enqueue[count]
        
        if baseline_time is not None and optimized_time is not None:
            speedup = baseline_time / optimized_time if optimized_time > 0 else 0
            print(f"{count:<12} | {baseline_time:<16.4f} | {optimized_time:<16.4f} | {speedup:<12.2f}x")
        else:
            print(f"{count:<12} | {'[ERROR]':<16} | {'[ERROR]':<16} | {'N/A':<12}")
    
    # ========== DEQUEUE ONLY TESTS ==========
    print("\n\n" + "=" * 90)
    print("DEQUEUE OPERATIONS - SERVE ALL PATIENTS")
    print("=" * 90)
    print("\nTest Configuration:")
    print("- Operation: Only DEQUEUE (Serve/remove patients from queue)")
    print("- Patient Severity: Random 1-5 (5 = critical)")
    print("- Random Seed: 42 (reproducible)")
    print("- Patient Counts: 10, 50, 100, 500, 1000")
    print("=" * 90)
    
    print("\n" + "[BASELINE - FIFO QUEUE DEQUEUE]".center(90, "-"))
    print("-" * 90)
    
    for count in patient_counts:
        print(f"Dequeue {count:4d} patients...", end=" ", flush=True)
        input_data = generate_baseline_input(count, measure_phase="dequeue")
        elapsed_time, success, error_msg = run_benchmark("baseline.py", input_data, count)
        
        if success and elapsed_time is not None:
            baseline_dequeue[count] = elapsed_time
            print(f"[OK] {elapsed_time:.4f}s ({elapsed_time*1000:.2f}ms)")
        else:
            baseline_dequeue[count] = None
            print(f"[FAILED]")
    
    print("\n" + "[OPTIMIZED - PRIORITY QUEUE DEQUEUE]".center(90, "-"))
    print("-" * 90)
    
    for count in patient_counts:
        print(f"Dequeue {count:4d} patients...", end=" ", flush=True)
        input_data = generate_optimized_input(count, measure_phase="dequeue")
        elapsed_time, success, error_msg = run_benchmark("optimized.py", input_data, count)
        
        if success and elapsed_time is not None:
            optimized_dequeue[count] = elapsed_time
            print(f"[OK] {elapsed_time:.4f}s ({elapsed_time*1000:.2f}ms)")
        else:
            optimized_dequeue[count] = None
            print(f"[FAILED]")
    
    # Results table - DEQUEUE
    print("\n" + "=" * 90)
    print("DEQUEUE RESULTS SUMMARY")
    print("=" * 90)
    print(f"{'Patients':<12} | {'Baseline (s)':<16} | {'Optimized (s)':<16} | {'Speedup':<12}")
    print("-" * 65)
    
    for count in patient_counts:
        baseline_time = baseline_dequeue[count]
        optimized_time = optimized_dequeue[count]
        
        if baseline_time is not None and optimized_time is not None:
            speedup = baseline_time / optimized_time if optimized_time > 0 else 0
            print(f"{count:<12} | {baseline_time:<16.4f} | {optimized_time:<16.4f} | {speedup:<12.2f}x")
        else:
            print(f"{count:<12} | {'[ERROR]':<16} | {'[ERROR]':<16} | {'N/A':<12}")
    
    # Summary statistics
    print("\n" + "=" * 90)
    print("OVERALL STATISTICS")
    print("=" * 90)
    
    valid_baseline_enqueue = [t for t in baseline_enqueue.values() if t is not None]
    valid_optimized_enqueue = [t for t in optimized_enqueue.values() if t is not None]
    valid_baseline_dequeue = [t for t in baseline_dequeue.values() if t is not None]
    valid_optimized_dequeue = [t for t in optimized_dequeue.values() if t is not None]
    
    if valid_baseline_enqueue and valid_optimized_enqueue:
        print("\n[ENQUEUE PERFORMANCE]")
        baseline_enqueue_total = sum(valid_baseline_enqueue)
        optimized_enqueue_total = sum(valid_optimized_enqueue)
        enqueue_speedup = baseline_enqueue_total / optimized_enqueue_total if optimized_enqueue_total > 0 else 0
        print(f"  Baseline Total:  {baseline_enqueue_total:.4f}s")
        print(f"  Optimized Total: {optimized_enqueue_total:.4f}s")
        print(f"  Speedup:         {enqueue_speedup:.2f}x")
        if enqueue_speedup > 1:
            print(f"  Result:          Baseline is {enqueue_speedup:.2f}x faster")
        else:
            print(f"  Result:          Optimized is {1/enqueue_speedup:.2f}x faster")
    
    if valid_baseline_dequeue and valid_optimized_dequeue:
        print("\n[DEQUEUE PERFORMANCE]")
        baseline_dequeue_total = sum(valid_baseline_dequeue)
        optimized_dequeue_total = sum(valid_optimized_dequeue)
        dequeue_speedup = baseline_dequeue_total / optimized_dequeue_total if optimized_dequeue_total > 0 else 0
        print(f"  Baseline Total:  {baseline_dequeue_total:.4f}s")
        print(f"  Optimized Total: {optimized_dequeue_total:.4f}s")
        print(f"  Speedup:         {dequeue_speedup:.2f}x")
        if dequeue_speedup > 1:
            print(f"  Result:          Baseline is {dequeue_speedup:.2f}x faster")
        else:
            print(f"  Result:          Optimized is {1/dequeue_speedup:.2f}x faster")
    
    if valid_baseline_enqueue and valid_baseline_dequeue and valid_optimized_enqueue and valid_optimized_dequeue:
        print("\n[COMBINED PERFORMANCE]")
        baseline_combined = sum(valid_baseline_enqueue) + sum(valid_baseline_dequeue)
        optimized_combined = sum(valid_optimized_enqueue) + sum(valid_optimized_dequeue)
        combined_speedup = baseline_combined / optimized_combined if optimized_combined > 0 else 0
        print(f"  Baseline Total:  {baseline_combined:.4f}s")
        print(f"  Optimized Total: {optimized_combined:.4f}s")
        print(f"  Speedup:         {combined_speedup:.2f}x")
        if combined_speedup > 1:
            print(f"  Result:          Baseline is {combined_speedup:.2f}x faster overall")
        else:
            print(f"  Result:          Optimized is {1/combined_speedup:.2f}x faster overall")
    
    print("\n" + "=" * 90)

if __name__ == "__main__":
    main()
