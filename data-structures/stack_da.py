# Name: Riley Ovenshire
# OSU Email: ovenshir@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: 5/8/2023 @ 11.59 PM
# Description: Implementing a singly linked list, stack ADT and queue ADT.

from dynamic_array import *


class StackException(Exception):
    """
    Custom exception to be used by Stack class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass


class Stack:
    def __init__(self):
        """
        Init new stack based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._da = DynamicArray()

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "STACK: " + str(self._da.length()) + " elements. ["
        out += ', '.join([str(self._da[i]) for i in range(self._da.length())])
        return out + ']'

    def is_empty(self) -> bool:
        """
        Return True is the stack is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.is_empty()

    def size(self) -> int:
        """
        Return number of elements currently in the stack
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.length()

    # -----------------------------------------------------------------------

    def push(self, value: object) -> None:
        """
        Adds a new value to the top of the stack, O(1).

        Receives: value to add
        Returns: nothing
        """
        # use dynamic array methods
        self._da.append(value)


    def pop(self) -> object:
        """
        Removes the top element of the stack, retursn its value. O(1) complexity. Raises exception if stack is empty.

        Receives: nothing
        Returns: value that was removed
        """
        # check if stack is empty
        if self._da.is_empty():
            raise StackException

        for index in range(self._da.length()):
            removal = self._da.get_at_index(self._da.length() - 1)
            self._da.remove_at_index(self._da.length() - 1)
            return removal

    def top(self) -> object:
        """
        Returns valueof the top element without removing it, O(1) complexity. Raises exception if stack is empty.

        Receives: nothing
        Returns: value of top element
        """
        # check if stack is empty
        if self._da.is_empty():
            raise StackException

        # same as pop but without removal
        top = self._da.get_at_index(self._da.length() - 1)
        return top


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# push example 1")
    s = Stack()
    print(s)
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    print(s)

    print("\n# pop example 1")
    s = Stack()
    try:
        print(s.pop())
    except Exception as e:
        print("Exception:", type(e))
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    for i in range(6):
        try:
            print(s.pop())
        except Exception as e:
            print("Exception:", type(e))

    print("\n# top example 1")
    s = Stack()
    try:
        s.top()
    except Exception as e:
        print("No elements in stack", type(e))
    s.push(10)
    s.push(20)
    print(s)
    print(s.top())
    print(s.top())
    print(s)
