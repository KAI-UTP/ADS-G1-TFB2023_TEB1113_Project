from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Patient:
    """
    Patient model shared by baseline and optimized systems.
    """
    id: int
    name: str
    severity: int      # 1 (low) to 5 (critical)
    arrival_time: int  # increasing counter or timestamp


class _Node:
    def __init__(self, data: Patient) -> None:
        self.data: Patient = data
        self.next_ptr: Optional["_Node"] = None
        self.prev_ptr: Optional["_Node"] = None


class FCFSTriageSystem:
    """
    First-Come-First-Serve triage system using a doubly linked list queue.
    """

    def __init__(self, max_capacity: Optional[int] = None) -> None:
        self.head: Optional[_Node] = None
        self.tail: Optional[_Node] = None
        self._size: int = 0
        self._capacity: Optional[int] = max_capacity

    def is_full(self) -> bool:
        return self._capacity is not None and self._size >= self._capacity

    def is_empty(self) -> bool:
        return self._size == 0

    def arrive(self, patient: Patient) -> None:
        if self.is_full():
            print("Queue overflow! Cannot enqueue new patient.")
            return

        new_node = _Node(patient)

        if self.head is None:
            self.head = self.tail = new_node
        else:
            assert self.tail is not None
            self.tail.next_ptr = new_node
            new_node.prev_ptr = self.tail
            self.tail = new_node

        self._size += 1

    def serve_next(self) -> Optional[Patient]:
        if self.head is None:
            print("Queue underflow! No patients to serve.")
            return None

        node = self.head
        self.head = node.next_ptr

        if self.head is not None:
            self.head.prev_ptr = None
        else:
            self.tail = None

        self._size -= 1
        return node.data

    def __len__(self) -> int:
        return self._size

    def traverse_forward(self) -> List[Patient]:
        result: List[Patient] = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next_ptr
        return result

    def traverse_backward(self) -> List[Patient]:
        result: List[Patient] = []
        current = self.tail
        while current is not None:
            result.append(current.data)
            current = current.prev_ptr
        return result

    def display(self) -> None:
        if self.is_empty():
            print("\nQueue is empty!")
            return

        print("\nQueue elements (front to rear):")
        current = self.head
        while current is not None:
            p = current.data
            print(f"  id={p.id}, name={p.name}, severity={p.severity}")
            current = current.next_ptr

    def get_current_size(self) -> int:
        return self._size

    def get_max_size(self) -> Optional[int]:
        return self._capacity


def read_int(prompt: str, min_val: Optional[int] = None,
             max_val: Optional[int] = None) -> int:
    while True:
        raw = input(prompt)
        try:
            value = int(raw)
        except ValueError:
            print("Invalid number. Try again.")
            continue

        if min_val is not None and value < min_val:
            print("Out of range. Try again.")
            continue
        if max_val is not None and value > max_val:
            print("Out of range. Try again.")
            continue

        return value


def read_non_empty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input cannot be empty. Try again.")


if __name__ == "__main__":
    print("=== FCFS Triage System Demo (Baseline) ===\n")

    arrival_counter = 0
    option = 0

    queue_size = read_int("Enter queue max capacity (e.g. 5 or 10): ", 1)
    system = FCFSTriageSystem(queue_size)

    while option != 8:
        print("\nMenu:")
        print(" 1. Enqueue / Add patient")
        print(" 2. Dequeue / Serve next patient")
        print(" 3. Show front patient")
        print(" 4. Show rear patient")
        print(" 5. Check if queue is full")
        print(" 6. Check if queue is empty")
        print(" 7. Display queue (front to rear)")
        print(" 8. Exit")
        option = read_int("Enter option: ", 1, 8)

        if option == 1:
            print("\n-- Add new patient --")
            name = read_non_empty("Enter name: ")
            pid = read_int("Enter ID (integer): ")
            severity = read_int("Enter severity (1=low, 5=critical): ", 1, 5)
            arrival_counter += 1

            p = Patient(
                id=pid,
                name=name,
                severity=severity,
                arrival_time=arrival_counter,
            )
            system.arrive(p)

        elif option == 2:
            p = system.serve_next()
            if p is not None:
                print(
                    f"\nDequeued / Serving: id={p.id}, "
                    f"name={p.name}, severity={p.severity}"
                )

        elif option == 3:
            if system.is_empty():
                print("\nQueue is empty!")
            else:
                front_patient = system.traverse_forward()[0]
                print(
                    f"\nFront patient: id={front_patient.id}, "
                    f"name={front_patient.name}, severity={front_patient.severity}"
                )

        elif option == 4:
            if system.is_empty():
                print("\nQueue is empty!")
            else:
                rear_patient = system.traverse_backward()[0]
                print(
                    f"\nRear patient: id={rear_patient.id}, "
                    f"name={rear_patient.name}, severity={rear_patient.severity}"
                )

        elif option == 5:
            if system.is_full():
                print("\nQueue is FULL")
            else:
                print("\nQueue is NOT FULL")
            cap = system.get_max_size()
            cap_str = str(cap) if cap is not None else "No limit"
            print(
                f"Current Size: {system.get_current_size()}  "
                f"Max Capacity: {cap_str}"
            )

        elif option == 6:
            if system.is_empty():
                print("\nQueue is EMPTY")
            else:
                print("\nQueue is NOT EMPTY")
            cap = system.get_max_size()
            cap_str = str(cap) if cap is not None else "No limit"
            print(
                f"Current Size: {system.get_current_size()}  "
                f"Max Capacity: {cap_str}"
            )

        elif option == 7:
            system.display()

        elif option == 8:
            print("\nExiting FCFS demo.")
            break
