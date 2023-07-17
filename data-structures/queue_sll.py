# Name: Riley Ovenshire
# OSU Email: ovenshir@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: 5/8/2023 @ 11.59 PM
# Description: Implementing a singly linked list, stack ADT and queue ADT.

from SLNode import SLNode


class QueueException(Exception):
    """
    Custom exception to be used by Queue class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass


class Queue:
    def __init__(self):
        """
        Initialize new queue with head and tail nodes
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = None
        self._tail = None

    def __str__(self):
        """
        Return content of queue in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'QUEUE ['
        if not self.is_empty():
            node = self._head
            out = out + str(node.value)
            node = node.next
            while node:
                out = out + ' -> ' + str(node.value)
                node = node.next
        return out + ']'

    def is_empty(self) -> bool:
        """
        Return True is the queue is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._head is None

    def size(self) -> int:
        """
        Return number of elements currently in the queue
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        node = self._head
        length = 0
        while node:
            length += 1
            node = node.next
        return length

    # -----------------------------------------------------------------------

    def enqueue(self, value: object) -> None:
        """
        Add new value to end of queue. O(1) complexity.

        Receives: value to add
        Returns: nothing
        """
        new_node = SLNode(value)
        if self.is_empty():
            self._head = new_node
            self._tail = new_node

        # same as stack, update next
        else:
            self._tail.next = new_node
        self._tail = new_node

    def dequeue(self) -> object:
        """
        Removes and returns value from front of queue. O(1) complexity. If empty, raise exception.

        Receives: nothing
        Returns: value removed
        """
        if self.is_empty():
            raise QueueException

        # same as stack, update next
        else:
            value = self._head.value
            self._head = self._head.next
            if self._head is None:
                self._tail = None
            return value

    def front(self) -> object:
        """
        Returns value from front of queue. O(1) complexity. If empty, raise exception.

        Receives: nothing
        Returns: value at front of queue
        """
        if self.is_empty():
            raise QueueException
        # same as before
        else:
            return self._head.value


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# enqueue example 1")
    q = Queue()
    print(q)
    for value in [1, 2, 3, 4, 5]:
        q.enqueue(value)
    print(q)

    print("\n# dequeue example 1")
    q = Queue()
    for value in [1, 2, 3, 4, 5]:
        q.enqueue(value)
    print(q)
    for i in range(6):
        try:
            print(q.dequeue())
        except Exception as e:
            print("No elements in queue", type(e))

    print('\n#front example 1')
    q = Queue()
    print(q)
    for value in ['A', 'B', 'C', 'D']:
        try:
            print(q.front())
        except Exception as e:
            print("No elements in queue", type(e))
        q.enqueue(value)
    print(q)
