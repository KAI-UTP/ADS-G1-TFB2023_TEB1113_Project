# Hospital Patient Prioritization System (Triage)

## Course & Group Information

- **Course Code:** TFB2023  
- **Course Name:** Algorithm and Data Structure  
- **Semester:** September 2025  

- **Group Project Title:** Hospital Patient Prioritization System  
- **Group:** Group 5  
- **Lecturer:** Ms. Farahida Hanim MausoR  

### Group Members

| No. | Name                   | ID       | Course               |
|-----|------------------------|----------|----------------------|
| 1.  | William Wong Xiao Kang | 22010943 | Computer Engineering |
| 2.  | Chan Li Kai            | 22010900 | Computer Engineering |
| 3.  | Liang Yan Ee           | 22011522 | Computer Engineering |
| 4.  | Irvin Chang Hou Ceng   | 22012342 | Computer Engineering |
| 5.  | Lew Wei Cheng          | 24000270 | Computer Science     |

---

## How to Run the Programs

### Prerequisites
- Python 3.7 or higher
- Windows, macOS, or Linux

### Running the FCFS Triage System (Baseline)

The baseline implementation uses a First-Come-First-Serve (FIFO) queue for patient triage.

**Command:**
```bash
python baseline.py
```

**Usage:**
1. Enter the maximum queue capacity (e.g., 5, 10, etc.)
2. Use the menu to:
   - Add patients to the queue
   - Serve patients in FIFO order
   - View front/rear patients
   - Check queue status (full/empty)
   - Display all patients
   - View queue statistics
3. Type `9` to exit the program

**Example Workflow:**
```
> Enter queue max capacity: 5
> Enter your choice (1-9): 1
> Patient name: John Smith
> Patient ID: 101
> Severity (1-5): 3
[OK] Patient John Smith (ID: 101) added!
```

### Running the Priority Queue Triage System (Optimized)

The optimized implementation uses a heap-based priority queue that serves the highest severity patients first.

**Command:**
```bash
python optimized.py
```

**Setup:**
1. Enter the number of doctors in rotation (e.g., 2, 3, etc.)
2. Enter each doctor's name
3. Enter the maximum size for the service history stack

**Usage:**
1. Use the menu to:
   - Add patients to the priority queue
   - Update patient severity levels
   - Serve patients (highest severity first)
   - Compare Priority Queue vs FCFS ordering
   - View service history
   - Display patient data in different tree traversal orders (inorder, preorder, postorder)
2. Type `11` to exit the program

**Example Workflow:**
```
> Enter number of doctors in rotation: 1
> Doctor 1 name: Dr. Smith
> Enter max size of service history stack: 20
> Enter choice: 1
> Patient name: Alice Brown
> Patient ID: 201
> Severity (1-5): 4
[OK] Patient Alice Brown (ID: 201) added!
```

### Running the Benchmark Suite

To compare performance between baseline and optimized implementations across different patient loads:

**Command:**
```bash
python benchmark_combine.py
```

This will automatically test both systems with 10, 50, 100, 500, and 1000 patients, measuring:
- Enqueue (add patient) time
- Dequeue (serve patient) time
- Overall performance comparison

---
