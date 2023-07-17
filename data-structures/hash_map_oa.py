# Name: Riley Ovenshire
# OSU Email: ovenshir@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - HashMap Portfolio Assignment
# Due Date: 6/10 @ 1:59 AM CST
# Description: Implementation of a HashMap using separate chaining, open addressing, and quadratic probing.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class StopIteration(Exception):
    """
    Exception to catch index out of range error.
    """
    pass


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #


    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in a hash map. If key already exists, associated value must be replaced with new value.
        If a key is not in the map, it must be added.

        Table must be resized to double its current capacity when called, and when the load factor is greater than or
        equal to .5.

        Receives: key (str), value (object)
        Returns: nothing
        """
        # check if table needs to be resized, if load factor is >= .5
        if self.table_load() >= .5:
            self.resize_table(self._capacity * 2)

        new_entry = HashEntry(key, value)

        # use hash function to get initial index
        hashed_key_initial = self._hash_function(new_entry.key) % self._capacity

        # check if index is empty, if so, add key/value pair
        if self._buckets.get_at_index(hashed_key_initial) is None:
            self._buckets.set_at_index(hashed_key_initial, new_entry)
            self._size += 1
            return
        if self._buckets.get_at_index(hashed_key_initial).is_tombstone:
            self._buckets.set_at_index(hashed_key_initial, new_entry)
            self._size += 1
            return
        # check if index key matches new key, if so, replace value
        elif self._buckets.get_at_index(hashed_key_initial).key == new_entry.key:
            self._buckets.set_at_index(hashed_key_initial, new_entry)
            return
        # at this point, index must be full and key must not be found, probe to find next open index
        else:
            # use quadratic probing to find next open index
            # see Exploration - Hash Table Collisions
            # in this case, hashed_key is initial index, j = 1, 2, 3,...
            # capacity is our m
            # constant == j
            constant = 1
            for index in range(1, self._capacity):
                next_index = hashed_key_initial + constant ** 2
                if next_index >= self._capacity:
                    next_index = next_index % self._capacity
                if self._buckets.get_at_index(next_index) is None:  # should increase size
                    self._buckets.set_at_index(next_index, new_entry)
                    self._size += 1
                    return
                elif self._buckets.get_at_index(next_index).key == new_entry.key:  # don't increase size, just replace value
                    self._buckets.set_at_index(next_index, new_entry)
                    return
                else:
                    constant += 1

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.

        Receives: nothing
        Returns: load factor as a float
        """
        elements = 0
        capacity = self._capacity
        for index in range(capacity):
            if self._buckets.get_at_index(index) is not None:
                elements += 1

        load_factor = elements / capacity

        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the table.

        Receives: nothing
        Returns: number of empty buckets, int
        """
        empties = 0
        capacity = self._capacity
        for index in range(capacity):
            if self._buckets.get_at_index(index) is None:
                empties += 1

        return empties

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes capacity of table, rehashed key/value pairs and hash links. If new_capacity is less than current
        number of elements, method does nothing.

        If new_capacity is valid, make sure it is prime. If not, find next prime number.

        Receives: new_capacity (int)
        Returns: nothing
        """
        current = self._capacity
        if new_capacity < self._size:
            return

        # store old values
        old_da = self._buckets

        # check if new_capacity is prime, if not, find next prime
        if self._is_prime(new_capacity):
            pass
        else:
            new_capacity = self._next_prime(new_capacity)

        self._capacity = new_capacity
        self._buckets = DynamicArray()

        # fill new array with None so we can rehash and put
        for index in range(new_capacity):
            self._buckets.append(None)

        # reset size
        self._size = 0

        # rehash and put old values, using HashEntry properties
        for index in range(current):
            if old_da.get_at_index(index) is not None:
                if old_da.get_at_index(index).is_tombstone is True:
                    pass
                else:
                    self.put(old_da.get_at_index(index).key, old_da.get_at_index(index).value)
        return

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If key is not in the map, returns None.

        Receives: key (str)
        Returns: value associated with key (object)
        """
        # hash key to get index
        hashed_key = self._hash_function(key) % self._capacity

        found = False
        while not found:
            # check if key is at hashed_key index
            if self._buckets.get_at_index(hashed_key) is not None:
                if self._buckets.get_at_index(hashed_key).key == key:
                    if self._buckets.get_at_index(hashed_key).is_tombstone:
                        return None
                    found = True
                    return self._buckets.get_at_index(hashed_key).value
                elif self._buckets.get_at_index(hashed_key).key != key:
                    # if not, probe to find key
                    # use quadratic probing to find next open index
                    # see Exploration - Hash Table Collisions
                    # in this case, hashed_key is initial index, j = 1, 2, 3,...
                    # capacity is our m
                    # constant == j
                    constant = 1
                    for index in range(1, self._capacity):
                        next_index = hashed_key + constant ** 2
                        if next_index >= self._capacity:
                            next_index = next_index % self._capacity
                        if self._buckets.get_at_index(next_index) is None:
                            return None
                        elif self._buckets.get_at_index(next_index).key == key:
                            if self._buckets.get_at_index(next_index).is_tombstone:
                                return None
                            found = True
                            return self._buckets.get_at_index(next_index).value
                        else:
                            constant += 1
            else:
                return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the map, otherwise returns False.

        Receives: key (str)
        Returns: True if key is in map, False if not
        """
        if self._size == 0:
            return False


        # hash key to get index
        hashed_key = self._hash_function(key) % self._capacity

        # Exploration - Hash Table Collisions video for reference
        # check if key is at hashed_key index
        if self._buckets.get_at_index(hashed_key) is not None:
            if self._buckets.get_at_index(hashed_key).key == key:
                return True
            elif self._buckets.get_at_index(hashed_key).key != key:
                # if not, probe to find key
                # use quadratic probing to find next open index
                # see Exploration - Hash Table Collisions
                # in this case, hashed_key is initial index, j = 1, 2, 3,...
                # capacity is our m
                # constant == j
                constant = 1
                for index in range(1, self._capacity):
                    next_index = hashed_key + constant ** 2
                    if next_index >= self._capacity:
                        next_index = next_index % self._capacity
                    if self._buckets.get_at_index(next_index) is None:
                        return False
                    elif self._buckets.get_at_index(next_index).key == key:
                        return True
                    else:
                        constant += 1
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes the key and its value. If key is not in the map, do nothing.

        Receives: key (str)
        Returns: nothing
        """
        if self._size == 0:
            return
        if not self.contains_key(key):
            return

        # hash key to get index
        hashed_key = self._hash_function(key) % self._capacity

        # Exploration - Hash Table Collisions video for reference, especially regarding tombstones


        if self._buckets.get_at_index(hashed_key).is_tombstone and self._buckets.get_at_index(hashed_key).key == key:
            return

        # check if key is at hashed_key index
        if self._buckets.get_at_index(hashed_key) is not None:
            if self._buckets.get_at_index(hashed_key).key == key:
                # give this object the tombstone value True
                self._buckets.get_at_index(hashed_key).is_tombstone = True
                self._size -= 1
                return
            elif self._buckets.get_at_index(hashed_key).key != key:
                # if not, probe to find key
                # use quadratic probing to find next open index
                # see Exploration - Hash Table Collisions
                # in this case, hashed_key is initial index, j = 1, 2, 3,...
                # capacity is our m
                # constant == j
                constant = 1
                for index in range(0, self._capacity):
                    next_index = hashed_key + constant ** 2
                    if next_index >= self._capacity:
                        next_index = next_index % self._capacity

                    # if next index is None, stop probing
                    if self._buckets.get_at_index(next_index) is None:
                        return
                    # if next index is not key, move on
                    if self._buckets.get_at_index(next_index).key != key or self._buckets.get_at_index(next_index).is_tombstone is True:
                        constant += 1
                    if self._buckets.get_at_index(next_index).key == key:
                        # see if it is already a tombstone
                        if self._buckets.get_at_index(next_index).is_tombstone:
                            return
                        # if not, give it a tombstone
                        else:
                            self._buckets.get_at_index(next_index).is_tombstone = True
                            self._size -= 1
                            return


    def clear(self) -> None:
        """
        Removes all items from the map, does not change underlying capacity.

        Receives: nothing
        Returns: nothing
        """
        for index in range(self._capacity):
            self._buckets.set_at_index(index, None)

        self._size = 0

        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a dynamic array where each index is a tuple of key and val. Order doesn't matter.

        Receives: nothing
        Returns: DynamicArray of tuples
        """
        pairs = DynamicArray()

        for index in range(self._capacity):
            if self._buckets.get_at_index(index) is not None:
                if self._buckets.get_at_index(index).is_tombstone is False:
                    pairs.append((self._buckets.get_at_index(index).key, self._buckets.get_at_index(index).value))

        return pairs

    def __iter__(self):
        """
        Allows the hash map to iterate across itself. Reference Exploration - Encapsulation and Iterators as needed.
        Use a variable to track the iterator's progress.

        Receives: nothing
        Returns: nothing
        """
        # Exploration - Encapsulation and Iterators
        self._index = 0
        return self

    def __next__(self):
        """
        Return the next item in the map depending on the location of the iterator. Only needs to iterate over active
        items.

        Receives: nothing
        Returns: next item in map
        """
        # Exploration - Encapsulation and Iterators
        try:
            while self._index < self._capacity - 1:
                value = self._buckets.get_at_index(self._index)
                if value is None:
                    self._index += 1
                    if self._buckets.get_at_index(self._index) is None:
                        break
                elif value.is_tombstone:
                    self._index += 1
                    if self._buckets.get_at_index(self._index) is None:
                        break
            self._index += 1
            return value

        except DynamicArrayException:
            raise StopIteration






# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
