import heapq
from typing import Optional, List, Tuple

from baseline import Patient, FCFSTriageSystem, read_int, read_non_empty


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
            print("History stack overflow! Cannot push new record.")
            return
        new_node = _StackNode(value)
        new_node.next_ptr = self._head
        self._head = new_node
        self._size += 1
        print(f"\n[History] Pushed: {value}")

    def pop(self) -> Optional[str]:
        if self.is_empty():
            print("History stack underflow! Cannot pop.")
            return None
        assert self._head is not None
        popped_value = self._head.data
        self._head = self._head.next_ptr
        self._size -= 1
        print(f"\n[History] Popped record: {popped_value}")
        return popped_value

    def peek(self) -> Optional[str]:
        if self.is_empty():
            print("History stack is empty!")
            return None
        assert self._head is not None
        print(f"\n[History] Top record: {self._head.data}")
        return self._head.data

    def is_full(self) -> bool:
        return self._size >= self._capacity

    def is_empty(self) -> bool:
        return self._head is None

    def display(self) -> None:
        if self.is_empty():
            print("\n[History] Stack is empty!")
            return
        print("\n[History] Stack elements (most recent first):")
        current = self._head
        while current is not None:
            print(" ", current.data)
            current = current.next_ptr

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
    print("=== Priority Queue Triage System Demo (Optimized) ===\n")

    num_docs = read_int("Enter number of doctors in rotation: ", 1)
    doctor_names: List[str] = []
    for i in range(num_docs):
        name = read_non_empty(f"Enter name for doctor {i + 1}: ")
        doctor_names.append(name)

    doctor_rotation = DoctorRotation(doctor_names)
    print("\nDoctor rotation set as circular list:")
    print("One cycle: ", end="")
    for _ in range(num_docs):
        print(doctor_rotation.next_doctor(), end=" ")
    print("\n(then it repeats in the same order)\n")

    history_size = read_int("Enter max size of service history stack: ", 1)
    history_stack = ServedHistoryStack(history_size)

    patient_bst = PatientBST()
    arrival_counter = 0
    pq = PriorityTriageSystem()

    while True:
        print("\nMenu:")
        print(" 1. Add patient")
        print(" 2. Update patient severity")
        print(" 3. Serve next patient")
        print(" 4. Compare PQ vs FCFS (current waiting list)")
        print(" 5. Show service history stack")
        print(" 6. Pop top history record")
        print(" 7. Peek top history record")
        print(" 8. Show BST Inorder traversal")
        print(" 9. Show BST Preorder traversal")
        print("10. Show BST Postorder traversal")
        print("11. Exit")

        choice = read_int("Enter choice: ", 1, 11)

        if choice == 1:
            name = read_non_empty("Enter patient name: ")
            pid = read_int("Enter patient ID (integer): ")
            severity = read_int("Enter severity (1=low, 5=critical): ", 1, 5)
            arrival_counter += 1

            p = Patient(
                id=pid,
                name=name,
                severity=severity,
                arrival_time=arrival_counter,
            )
            pq.arrive(p)
            patient_bst.insert(p)
            print("Patient added to priority queue and BST.\n")

        elif choice == 2:
            pid = read_int("Enter patient ID to update: ")
            new_sev = read_int("Enter new severity (1=low, 5=critical): ", 1, 5)
            updated_pq = pq.update_severity(pid, new_sev)
            updated_bst = patient_bst.update_severity(pid, new_sev)
            if updated_pq or updated_bst:
                print("Severity updated.\n")
            else:
                print("Patient not found.\n")

        elif choice == 3:
            patient = pq.serve_next()
            if patient is None:
                print("No patients waiting.\n")
            else:
                doctor = doctor_rotation.next_doctor()
                record = (
                    f"Patient(id={patient.id}, name={patient.name}, "
                    f"sev={patient.severity}) served by Dr. {doctor}"
                )
                print(
                    f"Serving (PQ): id={patient.id}, name={patient.name}, "
                    f"severity={patient.severity}, assigned doctor={doctor}\n"
                )
                history_stack.push(record)
                patient_bst.delete_by_id(patient.id)

        elif choice == 4:
            print("\n--- Compare FCFS vs Priority (current waiting list) ---")
            temp_patients: List[Patient] = [entry[2] for entry in pq._heap]

            if not temp_patients:
                print("No patients in queue to compare.\n")
                continue

            fcfs = FCFSTriageSystem()
            for p in sorted(temp_patients, key=lambda x: x.arrival_time):
                fcfs.arrive(p)

            print("FCFS order:")
            for p in fcfs.traverse_forward():
                print(f"  id={p.id}, name={p.name}, severity={p.severity}")

            print("\nPriority Queue order:")
            heap_copy = list(pq._heap)
            heapq.heapify(heap_copy)
            while heap_copy:
                _, _, p = heapq.heappop(heap_copy)
                print(f"  id={p.id}, name={p.name}, severity={p.severity}")
            print()

        elif choice == 5:
            history_stack.display()
            print(
                f"\n[History] Current size: {history_stack.get_current_size()} "
                f"/ {history_stack.get_max_size()}"
            )

        elif choice == 6:
            history_stack.pop()

        elif choice == 7:
            history_stack.peek()

        elif choice == 8:
            if patient_bst.is_empty():
                print("\nBST is empty!")
            else:
                print("\nBST Inorder (sorted by patient ID):")
                for p in patient_bst.inorder():
                    print(f"  id={p.id}, name={p.name}, severity={p.severity}")

        elif choice == 9:
            if patient_bst.is_empty():
                print("\nBST is empty!")
            else:
                print("\nBST Preorder:")
                for p in patient_bst.preorder():
                    print(f"  id={p.id}, name={p.name}, severity={p.severity}")

        elif choice == 10:
            if patient_bst.is_empty():
                print("\nBST is empty!")
            else:
                print("\nBST Postorder:")
                for p in patient_bst.postorder():
                    print(f"  id={p.id}, name={p.name}, severity={p.severity}")

        elif choice == 11:
            print("Exiting optimized demo.")
            break

