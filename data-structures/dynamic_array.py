# Name: Riley Ovenshire
# OSU Email: ovenshir@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 2 - Dynamic Array Implementation
# Due Date: 5/1 at 1:59 AM
# Description: Implementation of a dynamic array class with multiple methods provided in the skeleton code.


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Method that changes the capacity of the underlying storage for the elements in the dynamic array.

        Receives param: new capacity
        Returns: none, changes array capacity
        """
        # check for errors - if they're hit, do nothing with return
        if new_capacity <= 0:
            return  # why don't we raise the exception here?
        if new_capacity < self._size:
            return
        new_array = StaticArray(new_capacity)
        for element in range(self._size):
            # preserve data
            new_array[element] = self._data[element]
        self._data = new_array
        self._capacity = new_capacity

    def append(self, value: object) -> None:
        """
        This method will add a new value at the end of the dynamic array.

        Receives param: value to add
        Returns: none, but adds element to the end of the array and updates size/cap
        """
        if self._size == self._capacity:
            self.resize(self._capacity * 2)
        self._data[self._size] = value
        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Adds a new value at the specified index in a dynamic array.

        Receives param: index to be filled and the value to put there
        Returns: none but inserts element at given index, changes size/cap
        """
        # check for index issues
        if index < 0 or index > self._size:
            raise DynamicArrayException("Index is invalid.")
        if self._size == self._capacity:
            self.resize(self._capacity * 2)
        for element in range(self._size - 1, index - 1, -1):
            self._data[element + 1] = self._data[element]
        self._data[index] = value
        self._size += 1

    def remove_at_index(self, index: int) -> None:
        """
        Removes element at given index - if invalid there is a DynamicArrayException. Rules:
        - when elements stored in array is strictly less than 1/4 of the capacity, cap is reduced to twice the num of current elements.
        - if current cap is 10 or less, no reduction occurs.
        - if the cap is greater than 10, reduced cap cannot be less than 10.

        Receives param: index - index of element to be removed
        Returns: None but removes element from array and changes size/cap
        """
        # check for index issues
        if index < 0:
            raise DynamicArrayException("Index must be a positive integer.")
        if index >= self._size:
            raise DynamicArrayException("Index is out of range.")

        if self._size < (self._capacity / 4) and self._capacity > 10:

            # used edDiscussion #118 for reference
            new_capacity = max(self._size * 2, 10)
            new_array = StaticArray(new_capacity)
            for element in range(self._size):
                if element < index:
                    new_array[element] = self._data[element]
                else:
                    new_array[element] = self._data[element + 1]
            self._data = new_array
            self._capacity = new_capacity


        else:  # no need to resizae
            for element in range(index, self._size - 1):
                self._data[element] = self._data[element + 1]
        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Creates a new array that contains the requested number of elements from the original array.

        Receives param: start index to slice, size of slice
        Returns: new array with sliced elements
        """
        if start_index < 0:
            raise DynamicArrayException("Index cannot be less than 0.")
        if start_index >= self._size:
            raise DynamicArrayException("Index is too high.")
        if size < 0:
            raise DynamicArrayException("Size cannot be less than 0.")
        if start_index + size > self._size:
            raise DynamicArrayException("Size exceeds capacity.")

        new_array = DynamicArray()
        # take elements from index to index + size
        for element in range(start_index, start_index + size):
            new_array.append(self._data[element])
        return new_array

    def merge(self, second_da: "DynamicArray") -> None:
        """
        Takes another dynamic array and appends all elements from this array onto the current one, in the same order

        Receives param: another array
        Returns: nothing but changes current array with merged elements
        """
        second_size = second_da._size
        # take all elements, append them from it onto the current
        for element in range(second_size):
            self.append(second_da[element])

    def map(self, map_func) -> "DynamicArray":
        """
        Creates a new dynamic array where the value of each element is derived by applying a map function to the corresponding value.

        From Python documentation (for my own reference):
            Return an iterator that applies function to every item of iterable, yielding the results.
        If additional iterables arguments are passed, function must take that many arguments and is applied to the items from
        all iterables in parallel. With multiple iterables, the iterator stops when the shortest iterable is exhausted.

        Receives param: map function
        Returns: new array with elements that have been mapped according to function
        """
        new_array = DynamicArray()
        # use map_func for adding elements in the data
        for element in range(self._size):
            new_array.append(map_func(self._data[element]))
        return new_array

    def filter(self, filter_func) -> "DynamicArray":
        """
        Create new array with only the elements that return True after handled by filter.

        From Python documentation (for my own reference):
            Construct an iterator from those elements of iterable for which function is true. iterable may be either a sequence,
            a container which supports iteration, or an iterator.
            If function is None, the identity function is assumed, that is, all elements of iterable that are false are removed.

        Receives param: filter function
        Returns: array with filtered elements
        """
        new_array = DynamicArray()
        # use filter_func for adding elements in the data, if true then add and return array
        for element in range(self._size):
            if filter_func(self._data[element]) is True:
                new_array.append(self._data[element])
            elif filter_func is None:
                pass
        return new_array

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Applies reduction function to elements in the array and returns the resulting value. If no initializer is given, first element is used as initializer.

        Receives param: reduction function, init (or None by default)
        Returns: resulting reduction
        """
        if self._size > 0:
            reduction = self._data[0]  # first element is init
        elif self._size == 0:  # method returns val of init since array is empty
            return initializer
        else:  # otherwise use initializer
            reduction = initializer

        if initializer is not None:
            reduction = reduce_func(initializer, reduction)  # perform reduction on init and element
        for element in range(1, self._size):  # iterate
            reduction = reduce_func(reduction, self._data[element])
        return reduction

    @property
    def size(self):
        return self._size

    def da_pop(self):
        """
        Pops last element off of array.
        """
        if self._size == 0:
            raise DynamicArrayException("Array is empty.")
        else:
            last_element = self._data[self._size - 1]
            self.remove_at_index(self._size - 1)



def find_mode(arr: DynamicArray) -> (DynamicArray, int):
    """
    Receives sorted dynamic array, returns a tuple containing:
        1. dynamic array with mode of array
        2. int that represents highest frequency of value
        *** if there is more than one more, return the one that appears first
        O(n) complexity

        see edD #76 for reference

        Receives param: array
        Returns: tuple with array of mode and its frequency
    """
    mode_array = DynamicArray()
    mode_element = arr[0]
    mode_count = 0
    current = arr[0]
    counter = 1

    for element in range(1, arr._size):
        if arr[element] == current:
            counter += 1
        else:
            if counter > mode_count:
                # clear previous values of array and update, otherwise just add
                mode_array = DynamicArray()
                mode_array.append(current)
                mode_count = counter
            elif counter == mode_count:
                mode_array.append(current)

            #reset
            current = arr[element]
            counter = 1

# can be exact same as above
    if counter > mode_count:
        mode_array = DynamicArray()
        mode_array.append(current)
        mode_count = counter
    elif counter == mode_count:
        mode_array.append(current)

    return mode_array, mode_count


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)

    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
