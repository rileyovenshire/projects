# Name: Riley Ovenshire
# OSU Email: ovenshir@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 2 - Dynamic Array Implementation
# Due Date: 5/1 at 1:59 AM
# Description: Implementation of a dynamic array class with multiple methods provided in the skeleton code.


from dynamic_array import *


class Bag:
    def __init__(self, start_bag=None):
        """
        Init new bag based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._da = DynamicArray()

        # populate bag with initial values (if provided)
        # before using this feature, implement add() method
        if start_bag is not None:
            for value in start_bag:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "BAG: " + str(self._da.length()) + " elements. ["
        out += ', '.join([str(self._da.get_at_index(_))
                          for _ in range(self._da.length())])
        return out + ']'

    def size(self) -> int:
        """
        Return total number of items currently in the bag
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.length()

    # -----------------------------------------------------------------------

    def add(self, value: object) -> None:
        """
        Adds a new element to the bag with O(1) time complexity

        Receives: self._da (array value in init) + value to be added
        Returns: nothing, just adds value
        """
        self._da.append(value)

    def remove(self, value: object) -> bool:
        """
        Removes an element from bag with O(n) time complexity

        Receives: self._da (array value in init) + value to be removed
        Returns: True if value is removed, False if not
        """
        for index in range(self._da.length()):
            if self._da.get_at_index(index) == value:
                self._da.remove_at_index(index)
                return True
        return False


    def count(self, value: object) -> int:
        """
        Method returns the number of elements in the bag that have the same value as the desired one.

        Receives: self._da (array value in init) + desired value
        Returns: number of elements in bag with desired value
        """
        amount = 0
        for index in range(self._da.length()):
            if self._da.get_at_index(index) == value:
                amount += 1
        return amount

    def clear(self) -> None:
        """
        Clear the contents of the bag

        Receives: self._da (array value in init)
        Returns: nothing, just clears the bag by creating a new dynamic array (hopefully that is okay)
        """
        self._da = DynamicArray()       # simply declare new array

    def equal(self, second_bag: "Bag") -> bool:
        """
        Compare two bags, return True if they contain the same number of elements and same elements regardless of order
        Otherwise, return False. Empty bags are equal when compared to other empty bags.
        Rules:
            - cannot change the contents of bags
            - cannot create additional structures
            - o(n^2) complexity

        Receives: self._da + bag to be compared
        Returns: True if bags are equal, False if not
        """
        if self._da.length() != second_bag._da.length():      # if lengths are not equal, automatically know they're not equal
            return False
        for index in range(self._da.length()):                # loop through first bag
            index_counted = self._da.get_at_index(index)
            if self.count(index_counted) != second_bag.count(index_counted):     # if count of value in first bag is not equal to count of value in second bag, return False
                return False
        return True

    def __iter__(self):
        """
        Allows bag to iterate over itself, use Exploration: Encapsulation and Iterators for reference
        Need to init a variable to track progrss through contents

        Receives: self._da (array value in init)
        Returns: nothing just allows iteration through bag
        """
        # exploration used as reference
        self._index = 0

        return self

    def __next__(self):
        """
        Use iterator to return the next item in the bag based on location of iterator, use Exploration: Encapsulation and Iterators for reference

        Receives: self._da (array value in init)
        Returns: next item in bag
        """
        # exploration used as reference
        try:
            value = self._da[self._index]
        except DynamicArrayException:
            raise StopIteration()

        self._index += 1
        return value


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# add example 1")
    bag = Bag()
    print(bag)
    values = [10, 20, 30, 10, 20, 30]
    for value in values:
        bag.add(value)
    print(bag)

    print("\n# remove example 1")
    bag = Bag([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(bag)
    print(bag.remove(7), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)

    print("\n# count example 1")
    bag = Bag([1, 2, 3, 1, 2, 2])
    print(bag, bag.count(1), bag.count(2), bag.count(3), bag.count(4))

    print("\n# clear example 1")
    bag = Bag([1, 2, 3, 1, 2, 3])
    print(bag)
    bag.clear()
    print(bag)

    print("\n# equal example 1")
    bag1 = Bag([10, 20, 30, 40, 50, 60])
    bag2 = Bag([60, 50, 40, 30, 20, 10])
    bag3 = Bag([10, 20, 30, 40, 50])
    bag_empty = Bag()

    print(bag1, bag2, bag3, bag_empty, sep="\n")
    print(bag1.equal(bag2), bag2.equal(bag1))
    print(bag1.equal(bag3), bag3.equal(bag1))
    print(bag2.equal(bag3), bag3.equal(bag2))
    print(bag1.equal(bag_empty), bag_empty.equal(bag1))
    print(bag_empty.equal(bag_empty))
    print(bag1, bag2, bag3, bag_empty, sep="\n")

    bag1 = Bag([100, 200, 300, 200])
    bag2 = Bag([100, 200, 30, 100])
    print(bag1.equal(bag2))

    print("\n# __iter__(), __next__() example 1")
    bag = Bag([5, 4, -8, 7, 10])
    print(bag)
    for item in bag:
        print(item)

    print("\n# __iter__(), __next__() example 2")
    bag = Bag(["orange", "apple", "pizza", "ice cream"])
    print(bag)
    for item in bag:
        print(item)
