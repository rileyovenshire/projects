# Description: Implementation of a heap data structure using a dynamic array


from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        """
        self._heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return 'HEAP ' + str(heap_data)

    def add(self, node: object) -> None:
        """
        Adds a new object to the MinHeap, maintaining heap property. O(log(n))

        Receives: node to add
        Returns: nothing
        """

        # new element to the end of the array
        self._heap.append(node)
        node_index = self._heap.length() - 1

        # # repeat until the new element is the root or is greater than its parent
        while node_index > 0:
            parent_index = (node_index - 1) // 2                # floor div
            if self._heap[node_index] < self._heap[parent_index]:
                self._heap[node_index], self._heap[parent_index] = self._heap[parent_index], self._heap[node_index]
                node_index = parent_index
            else:
                break

    def is_empty(self) -> bool:
        """
        Returns True if the MinHeap is empty, False otherwise. O(1)

        Receives: nothing
        Returns: True if empty, False otherwise
        """
        if self._heap.is_empty():
            return True
        else:
            return False

    def get_min(self) -> object:
        """
        Returns the minimum value in the MinHeap without removing it. If the heap is empty, raises MinHeapException. O(1)

        Receives: nothing
        Returns: minimum value in the MinHeap
        """
        if self._heap.is_empty():
            raise MinHeapException("Heap is empty.")
        else:
            return self._heap[0]

    def remove_min(self) -> object:
        """
        Removes the minimum value in the MinHeap and returns it. If the heap is empty, raises MinHeapException. O(log(n))
        For the downward percolation of the replacement node: if both children of the node have
        the same value (and are both smaller than the node), swap with the left child.


        Receives: nothing
        Returns: minimum value in the MinHeap
        """
        if self._heap.is_empty():
            raise MinHeapException("Heap is empty.")

        minimum = self._heap[0]

        if self._heap.length() == 1:
            self._heap.da_pop()
            return minimum

        # use added da pop method
        self._heap[0] = self._heap[self._heap.length() - 1]
        self._heap.da_pop()

        _percolate_down(self._heap, 0, self._heap.length())

        return minimum

    def build_heap(self, da: DynamicArray) -> None:
        """
        Receives a DA with objects in any order, builds a heap from them. Content of current MinHeap is overwritten. O(n)

        Receives: unsorted DA
        Returns: nothing
        """
        # Exploration - Heap Implementation, Build Heap
        new_heap = DynamicArray()
        for element in da:
            new_heap.append(element)
        self._heap = new_heap

        invalid_index = (new_heap.length() // 2) - 1

        for index in range(invalid_index, -1, -1):
            _percolate_down(new_heap, index, new_heap.length())

    def size(self) -> int:
        """
        Returns the amount of items that are stored in the heap.

        Receives: Nothing
        Returns: Amount of elements in heap (int)
        """
        return self._heap.length()

    def clear(self) -> None:
        """
        Clears the contents of the heap. O(1)

        Receives: nothing
        Returns: nothing
        """
        self._heap = DynamicArray()


def heapsort(da: DynamicArray) -> None:
    """
    Receives an unsorted DA and sorts it in-place, non-ascending, using a MinHeap. O(nlog(n))
    Array will contain at least one element, all elements are same type.

    Receives: unsorted DA
    Returns: nothing
    """
    # Exploration - Heap Implementation, Heapsort
    # first, heapify the array using build_heap logic
    nonleaf = (da.length() // 2) - 1
    for index in range(nonleaf, -1, -1):
        _percolate_down(da, index, da.length())

    # keep a running counter of the last element in the array
    running_counter = da.length() - 1

    # while the running counter is greater than 0
    while running_counter > 0:
        # swap the first element with the last element
        da[0], da[running_counter] = da[running_counter], da[0]
        # decrement the running counter
        _percolate_down(da, 0, running_counter)
        running_counter -= 1

def _percolate_down(da: DynamicArray, parent: int, end: int) -> None:
    """
    Send the element at the specified index down the heap to its proper place. If both children of the node have
        the same value (and are both smaller than the node), swap with the left child.

    Receives: DynamicArray and index of element to percolate down
    Returns: nothing
    """
    index = parent


    while index < end:
        left_child = (2 * index) + 1
        right_child = (2 * index) + 2
        minimum_child = index

        if left_child < end and da[left_child] < da[minimum_child]:
            minimum_child = left_child

        if right_child < end and da[right_child] < da[minimum_child]:
            minimum_child = right_child

        if left_child < end and right_child < end and da[left_child] == da[right_child] and da[left_child] < da[minimum_child]:
            minimum_child = left_child

        if minimum_child == index:
            break

        da[index], da[minimum_child] = da[minimum_child], da[index]
        index = minimum_child


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)
