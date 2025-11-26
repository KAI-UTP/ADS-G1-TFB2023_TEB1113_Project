import os
import sys


def run_baseline() -> None:
    # Runs baseline.py as a separate Python process
    cmd = f'"{sys.executable}" baseline.py'
    os.system(cmd)


def run_optimized() -> None:
    # Runs optimized.py as a separate Python process
    cmd = f'"{sys.executable}" optimized.py'
    os.system(cmd)


def run_time_test() -> None:
    # Runs time_test.py as a separate Python process
    cmd = f'"{sys.executable}" time_test.py'
    os.system(cmd)


def main() -> None:
    while True:
        print("\n=== Hospital Triage System Launcher ===")
        print(" 1. Run Baseline FCFS demo")
        print(" 2. Run Optimized Priority Queue demo")
        print(" 3. Run Time Benchmark")
        print(" 4. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            run_baseline()
        elif choice == "2":
            run_optimized()
        elif choice == "3":
            run_time_test()
        elif choice == "4":
            print("Exiting launcher.")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
