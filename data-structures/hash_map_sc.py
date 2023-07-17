# Name: Riley Ovenshire
# OSU Email: ovenshir@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - HashMap Portfolio Assignment
# Due Date: 6/10 @ 1:59 AM CST
# Description: Implementation of a HashMap using separate chaining, open addressing, and quadratic probing.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Updates key/value pair in the hash map. If key is already in the map, value must be replaced with the new value.
        Table must be resized to double its current capacity when method is called and the load factor of the table
        is greater than or equal to 1.0.

        Receives: key (str), value (object)
        Returns: nothing
        """
        # Exploration - Introduction to Maps and Hash Tables (Hash Tables)

        # self._buckets is a DA of LinkedLists, cannot use for loop to iterate through by value
        # use for loop to iterate through LinkedLists

        # check if table needs to be resized, thank you TA Elliot Larsen for help!
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        # hash key to find bucket
        hashed_key = self._hash_function(key) % self._capacity

        # get bucket with hashed key
        bucket = self._buckets[hashed_key]

        # check if key is found in map
        if bucket.contains(key):
            index = bucket.contains(key)
            index.value = value

        # if not, insert
        else:
            bucket.insert(key, value)
            self._size += 1


    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        Receives: nothing
        Returns: number of empty buckets as an int
        """
        empties = 0
        # for whatever reason the iterator is disabled on the DA, so use for in range(self._buckets.length())
        for index in range(self._buckets.length()):
            bucket = self._buckets.get_at_index(index)
            if bucket is None or bucket.length() == 0:
                empties += 1
        return empties


    def table_load(self) -> float:
        """
        Returns the current hash table load factor.

        Receives: nothing
        Returns: load factor as a float
        """
        # lambda = lf, n = num elements, m = num buckets
        # lf = n/m
        elements = 0
        buckets = self._buckets.length()

        # find total number of elements, use range(self._buckets.length()) again
        for index in range(self._buckets.length()):
            bucket = self._buckets.get_at_index(index)
            for element in bucket:
                if element is None:
                    pass
                else:
                    elements += 1

        load_factor = elements / buckets

        return load_factor


    def clear(self) -> None:
        """
        Clears the contents of the hash map. Does not change capacity.

        Receives: nothing
        Returns: nothing
        """
        # clear contents, preserve capacity
        # for loop to iterate through DA
        for index in range(self._buckets.length()):
            bucket = self._buckets.get_at_index(index)
            for element in bucket:
                if element is None:
                    pass
                else:
                    bucket.remove(element.key)
                    self._size -= 1


    def resize_table(self, new_capacity: int) -> None:
        """
        Changes capacity of internal hash table, all key/value pairs must remain in the new hash map and all hash table
        links must be rehashed. If new_capacity is less than 1, method does nothing. If new_capacity is 1 or more,
        make sure it is a prime number, if not change it to the next highest prime number.

        Receives: new capacity as an int
        Returns: nothing
        """
        # Exploration - Introduction to Maps and Hash Tables (Hash Tables)
        # thank you TA Elliot Larsen for help!

        current_capacity = self._capacity
        # check if new_capacity is less than 1
        if new_capacity < 1:
            return

        # store existing content elsewhere
        old_da = self._buckets

        # check if new_capacity is prime
        if self._is_prime(new_capacity):
            pass
        # if not, change to next highest prime
        else:
            new_capacity = self._next_prime(new_capacity)

        self._capacity = new_capacity

        # reset buckets
        self._buckets = DynamicArray()

        # traverse buckets, append LL to each slot
        for index in range(new_capacity):
            self._buckets.append(LinkedList())

        # update size
        self._size = 0

        # re-insert nodes into new hashmap using self.put()
        for index in range(old_da.length()):
            bucket = old_da.get_at_index(index)
            for node in bucket:
                self.put(node.key, node.value)


    def get(self, key: str):
        """
        Returns the value associated with key. If key is not in the map, retrn None.

        Receives: key (str)
        Returns: value with key (object)
        """
        # hash key to find bucket
        hashed_key = self._hash_function(key) % self._capacity

        # get bucket with hashed key
        bucket = self._buckets[hashed_key]

        # if key is in map, return value
        found = False
        for index in range(self._buckets.length()):
            bucket = self._buckets.get_at_index(index)
            if bucket.contains(key):
                found = True
                return bucket.contains(key).value
        if not found:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns true if key is in the map, otherwise returns false.

        Receives: key (str)
        Returns: true if key is in map, false if not
        """
        # hash key to find bucket
        hashed_key = self._hash_function(key) % self._capacity

        # get bucket with hashed key
        bucket = self._buckets[hashed_key]

        # if key is in map, return value
        found = False
        for index in range(self._buckets.length()):
            bucket = self._buckets.get_at_index(index)
            if bucket.contains(key):
                found = True
        return found

    def remove(self, key: str) -> None:
        """
        Removes the given key/value pair from map, if not in map this method does nothing.

        Receives: key (str) to remove
        Returns: nothing
        """
        # hash key to find bucket
        hashed_key = self._hash_function(key) % self._capacity

        # get bucket with hashed key
        bucket = self._buckets[hashed_key]

        # if key is in map, return value
        found = False
        for index in range(self._buckets.length()):
            bucket = self._buckets.get_at_index(index)
            if bucket.contains(key):
                found = True
                bucket.remove(key)
                self._size -= 1

        if not found:
            return None


    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DA where each index is a tuple of key/value pairs from the map. Order does not matter.

        Receives: nothing
        Returns: DA of key/value pairs
        """
        pairs = DynamicArray()

        # iterate
        for index in range(self._buckets.length()):
            bucket = self._buckets.get_at_index(index)
            for element in bucket:
                pairs.append((element.key, element.value))
        return pairs



def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Receives an unsorted DA and returns a tuple containing (in this order):
    1. New DA containing the mode(s) of the original DA
    2. Int containing the frequency of the mode(s)

    If there is more than one mode, all values must be returned, order doesn't matter. If there is only one mode, return
    just that value. Array will always contain at least one value, all values will be strings, don't check for these.
    O(n) time complexity.

    Receives: unsorted DA of strings
    Returns: tuple containing (DA of mode(s), frequency of mode(s))

    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()

    # traverse DA, find frequencies, add to hashmap
    # O(n) time complexity because single for loop
    for index in range(da.length()):
        element = da.get_at_index(index)
        if map.contains_key(element):
            map.put(element, map.get(element) + 1)
        else:
            map.put(element, 1)

    # at this point, elements have been added like so,
    # key = element, value = frequency
        # or value[0] = element, value[1] = frequency

    # iterate through hashmap, find all modes
    mode_array = DynamicArray()
    max_mode = 1

    # O(n) time complexity because single for loop

    for index in range(map.get_size()):     # same as iterating by length
        value_array = map.get_keys_and_values()
        value = value_array.get_at_index(index)

        # value[0] = element, value[1] = frequency
        # catch value that is greater than first, so as not to add values of frequency 1
        if value[1] > max_mode:
            max_mode = value[1]
            # recreate DA in case first element was incorrectly added
            mode_array = DynamicArray()
            mode_array.append(value[0])
        elif value[1] == max_mode:
            mode_array.append(value[0])


    return (mode_array, max_mode)



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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
