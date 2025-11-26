import heapq
import sys
from typing import Optional, List, Tuple

from baseline import Patient, FCFSTriageSystem, read_int, read_non_empty, print_success, print_error, print_section

# Increase recursion limit for handling large datasets
sys.setrecursionlimit(2000)


class _DoctorNode:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.next_ptr: Optional["_DoctorNode"] = None


class DoctorRotation:
    """
    Circular singly linked list of doctors (round-robin assignment).
    """

    def __init__(self, doctor_names: List[str]) -> None:
        if not doctor_names:
            raise ValueError("At least one doctor is required.")

        self._nodes: List[_DoctorNode] = [
            _DoctorNode(name) for name in doctor_names
        ]

        for i in range(len(self._nodes)):
            nxt = self._nodes[(i + 1) % len(self._nodes)]
            self._nodes[i].next_ptr = nxt

        self._current: _DoctorNode = self._nodes[0]

    def next_doctor(self) -> str:
        name = self._current.name
        self._current = self._current.next_ptr  # type: ignore[assignment]
        return name


class _StackNode:
    def __init__(self, data: str) -> None:
        self.data: str = data
        self.next_ptr: Optional["_StackNode"] = None


class ServedHistoryStack:
    """
    Stack of service history records using a singly linked list.
    """

    def __init__(self, max_capacity: int) -> None:
        self._head: Optional[_StackNode] = None
        self._size: int = 0
        self._capacity: int = max_capacity

    def push(self, value: str) -> None:
        if self.is_full():
            print_error("History stack is full! Cannot push new record.")
            return
        new_node = _StackNode(value)
        new_node.next_ptr = self._head
        self._head = new_node
        self._size += 1

    def pop(self) -> Optional[str]:
        if self.is_empty():
            print_error("History stack is empty! Cannot pop.")
            return None
        assert self._head is not None
        popped_value = self._head.data
        self._head = self._head.next_ptr
        self._size -= 1
        return popped_value

    def peek(self) -> Optional[str]:
        if self.is_empty():
            print_error("History stack is empty!")
            return None
        assert self._head is not None
        return self._head.data

    def is_full(self) -> bool:
        return self._size >= self._capacity

    def is_empty(self) -> bool:
        return self._head is None

    def display(self) -> None:
        if self.is_empty():
            print_error("History stack is empty!")
            return
        print("\n  History Stack (most recent first):")
        current = self._head
        idx = 1
        while current is not None:
            print(f"    {idx}. {current.data}")
            current = current.next_ptr
            idx += 1

    def get_current_size(self) -> int:
        return self._size

    def get_max_size(self) -> int:
        return self._capacity


class _TreeNode:
    def __init__(self, patient: Patient) -> None:
        self.patient: Patient = patient
        self.left: Optional["_TreeNode"] = None
        self.right: Optional["_TreeNode"] = None


class PatientBST:
    """
    Binary Search Tree keyed by patient.id.
    """

    def __init__(self) -> None:
        self.root: Optional[_TreeNode] = None

    def insert(self, patient: Patient) -> None:
        self.root = self._insert(self.root, patient)

    def _insert(self, node: Optional[_TreeNode], patient: Patient) -> _TreeNode:
        if node is None:
            return _TreeNode(patient)
        if patient.id < node.patient.id:
            node.left = self._insert(node.left, patient)
        else:
            node.right = self._insert(node.right, patient)
        return node

    def delete_by_id(self, patient_id: int) -> None:
        self.root = self._delete(self.root, patient_id)

    def _delete(self, node: Optional[_TreeNode],
                patient_id: int) -> Optional[_TreeNode]:
        if node is None:
            return None

        if patient_id < node.patient.id:
            node.left = self._delete(node.left, patient_id)
        elif patient_id > node.patient.id:
            node.right = self._delete(node.right, patient_id)
        else:
            if node.left is None and node.right is None:
                return None
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.patient = successor.patient
            node.right = self._delete(node.right, successor.patient.id)
        return node

    def update_severity(self, patient_id: int, new_severity: int) -> bool:
        return self._update_severity(self.root, patient_id, new_severity)

    def _update_severity(
        self, node: Optional[_TreeNode], patient_id: int, new_severity: int
    ) -> bool:
        if node is None:
            return False
        if node.patient.id == patient_id:
            node.patient.severity = new_severity
            return True
        if patient_id < node.patient.id:
            return self._update_severity(node.left, patient_id, new_severity)
        else:
            return self._update_severity(node.right, patient_id, new_severity)

    def inorder(self) -> List[Patient]:
        result: List[Patient] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[_TreeNode],
                 result: List[Patient]) -> None:
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.patient)
            self._inorder(node.right, result)

    def preorder(self) -> List[Patient]:
        result: List[Patient] = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node: Optional[_TreeNode],
                  result: List[Patient]) -> None:
        if node is not None:
            result.append(node.patient)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self) -> List[Patient]:
        result: List[Patient] = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node: Optional[_TreeNode],
                   result: List[Patient]) -> None:
        if node is not None:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.patient)

    def is_empty(self) -> bool:
        return self.root is None


class PriorityTriageSystem:
    """
    Priority-based triage using a heap.
    """

    def __init__(self) -> None:
        self._heap: List[Tuple[Tuple[int, int], int, Patient]] = []
        self._counter: int = 0

    @staticmethod
    def _priority_for(patient: Patient) -> Tuple[int, int]:
        return -patient.severity, patient.arrival_time

    def arrive(self, patient: Patient) -> None:
        self._counter += 1
        entry = (self._priority_for(patient), self._counter, patient)
        heapq.heappush(self._heap, entry)

    def serve_next(self) -> Optional[Patient]:
        if not self._heap:
            return None
        _, _, patient = heapq.heappop(self._heap)
        return patient

    def update_severity(self, patient_id: int, new_severity: int) -> bool:
        found_index = -1
        for i, (prio, counter, patient) in enumerate(self._heap):
            if patient.id == patient_id:
                found_index = i
                break

        if found_index == -1:
            return False

        _, counter, patient = self._heap[found_index]
        patient.severity = new_severity

        new_entry = (self._priority_for(patient), counter, patient)
        self._heap[found_index] = new_entry
        heapq.heapify(self._heap)
        return True

    def is_empty(self) -> bool:
        return not self._heap

    def __len__(self) -> int:
        return len(self._heap)


if __name__ == "__main__":
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "="*60)
    print("  PRIORITY QUEUE TRIAGE SYSTEM (OPTIMIZED)")
    print("="*60 + "\n")

    num_docs = read_int("Enter number of doctors in rotation: ", 1)
    doctor_names = []
    for i in range(num_docs):
        name = read_non_empty(f"Doctor {i + 1} name: ")
        doctor_names.append(name)

    doctor_rotation = DoctorRotation(doctor_names)
    print_success("Doctor rotation set as circular list")
    print("  One cycle: ", end="")
    for _ in range(num_docs):
        print(doctor_rotation.next_doctor(), end=" ")
    print("\n  (then it repeats in the same order)\n")

    history_size = read_int("Enter max size of service history stack: ", 1)
    history_stack = ServedHistoryStack(history_size)

    patient_bst = PatientBST()
    arrival_counter = 0
    pq = PriorityTriageSystem()

    while True:
        print("\n" + "="*60)
        print("  MENU")
        print("="*60)
        print(" 1. Add patient")
        print(" 2. Update patient severity")
        print(" 3. Serve next patient")
        print(" 4. Compare Priority Queue vs FCFS")
        print(" 5. Show service history stack")
        print(" 6. Pop top history record")
        print(" 7. Peek top history record")
        print(" 8. Show BST Inorder traversal")
        print(" 9. Show BST Preorder traversal")
        print("10. Show BST Postorder traversal")
        print("11. Exit")
        print("="*60)

        choice = read_int("Enter choice: ", 1, 11)

        if choice == 1:
            print_section("ADD NEW PATIENT")
            name = read_non_empty("Patient name: ")
            pid = read_int("Patient ID (integer): ")
            severity = read_int("Severity (1=Low → 5=Critical): ", 1, 5)
            arrival_counter += 1

            p = Patient(
                id=pid,
                name=name,
                severity=severity,
                arrival_time=arrival_counter,
            )
            pq.arrive(p)
            patient_bst.insert(p)
            print_success(f"Patient {name} (ID: {pid}) added to priority queue and BST!")

        elif choice == 2:
            print_section("UPDATE PATIENT SEVERITY")
            pid = read_int("Patient ID to update: ")
            new_sev = read_int("New Severity (1=Low → 5=Critical): ", 1, 5)
            updated_pq = pq.update_severity(pid, new_sev)
            updated_bst = patient_bst.update_severity(pid, new_sev)
            if updated_pq or updated_bst:
                print_success(f"Patient {pid} severity updated to {new_sev}/5")
            else:
                print_error("Patient not found!")

        elif choice == 3:
            print_section("SERVE NEXT PATIENT")
            patient = pq.serve_next()
            if patient is None:
                print_error("No patients waiting!")
            else:
                doctor = doctor_rotation.next_doctor()
                record = (
                    f"ID={patient.id} | {patient.name} | "
                    f"Severity={patient.severity}/5 | Dr. {doctor}"
                )
                print_success(f"Now serving: {patient.name}")
                print(f"  ID: {patient.id} | Severity: {patient.severity}/5")
                print(f"  Assigned Doctor: Dr. {doctor}")
                history_stack.push(record)
                patient_bst.delete_by_id(patient.id)

        elif choice == 4:
            print_section("COMPARE PRIORITY QUEUE vs FCFS")
            temp_patients = [entry[2] for entry in pq._heap]

            if not temp_patients:
                print_error("No patients in queue to compare!")
                continue

            fcfs = FCFSTriageSystem()
            for p in sorted(temp_patients, key=lambda x: x.arrival_time):
                fcfs.arrive(p)

            print("\n  FCFS Order (First-Come-First-Served):")
            print("  " + "-"*90)
            print(f"  {'#':<4} | {'Name':<20} | {'ID':<5} | {'Severity':<18} | {'Arrival':<8}")
            print("  " + "-"*90)
            for i, p in enumerate(fcfs.traverse_forward(), 1):
                severity_str = "🔴" * p.severity + "⚪" * (5 - p.severity)
                print(f"  {i:<4} | {p.name:<20} | {p.id:<5} | {severity_str:<18} | #{p.arrival_time:<7}")
            print("  " + "-"*90)

            print("\n  Priority Queue Order (High Severity First):")
            print("  " + "-"*90)
            print(f"  {'#':<4} | {'Name':<20} | {'ID':<5} | {'Severity':<18} | {'Arrival':<8}")
            print("  " + "-"*90)
            heap_copy = list(pq._heap)
            heapq.heapify(heap_copy)
            idx = 1
            while heap_copy:
                _, _, p = heapq.heappop(heap_copy)
                severity_str = "🔴" * p.severity + "⚪" * (5 - p.severity)
                print(f"  {idx:<4} | {p.name:<20} | {p.id:<5} | {severity_str:<18} | #{p.arrival_time:<7}")
                idx += 1
            print("  " + "-"*90)

        elif choice == 5:
            print_section("SERVICE HISTORY STACK")
            history_stack.display()
            print(f"\n  Current size: {history_stack.get_current_size()} / {history_stack.get_max_size()}")

        elif choice == 6:
            print_section("POP TOP HISTORY RECORD")
            history_stack.pop()

        elif choice == 7:
            print_section("PEEK TOP HISTORY RECORD")
            history_stack.peek()

        elif choice == 8:
            print_section("BST - INORDER TRAVERSAL (Sorted by Patient ID)")
            if patient_bst.is_empty():
                print_error("BST is empty!")
            else:
                print("  " + "-"*90)
                print(f"  {'#':<4} | {'ID':<5} | {'Name':<20} | {'Severity':<18} | {'Arrival':<8}")
                print("  " + "-"*90)
                for i, p in enumerate(patient_bst.inorder(), 1):
                    severity_str = "🔴" * p.severity + "⚪" * (5 - p.severity)
                    print(f"  {i:<4} | {p.id:<5} | {p.name:<20} | {severity_str:<18} | #{p.arrival_time:<7}")
                print("  " + "-"*90)

        elif choice == 9:
            print_section("BST - PREORDER TRAVERSAL")
            if patient_bst.is_empty():
                print_error("BST is empty!")
            else:
                print("  " + "-"*90)
                print(f"  {'#':<4} | {'ID':<5} | {'Name':<20} | {'Severity':<18} | {'Arrival':<8}")
                print("  " + "-"*90)
                for i, p in enumerate(patient_bst.preorder(), 1):
                    severity_str = "🔴" * p.severity + "⚪" * (5 - p.severity)
                    print(f"  {i:<4} | {p.id:<5} | {p.name:<20} | {severity_str:<18} | #{p.arrival_time:<7}")
                print("  " + "-"*90)

        elif choice == 10:
            print_section("BST - POSTORDER TRAVERSAL")
            if patient_bst.is_empty():
                print_error("BST is empty!")
            else:
                print("  " + "-"*90)
                print(f"  {'#':<4} | {'ID':<5} | {'Name':<20} | {'Severity':<18} | {'Arrival':<8}")
                print("  " + "-"*90)
                for i, p in enumerate(patient_bst.postorder(), 1):
                    severity_str = "🔴" * p.severity + "⚪" * (5 - p.severity)
                    print(f"  {i:<4} | {p.id:<5} | {p.name:<20} | {severity_str:<18} | #{p.arrival_time:<7}")
                print("  " + "-"*90)

        elif choice == 11:
            print("\n" + "="*60)
            print("  Thank you for using Priority Triage System!")
            print("="*60 + "\n")
            break

