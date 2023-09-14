# Name: Ashton Stasko
# OSU Email: staskoa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 06/09/2023
# Description: Contains a class that represents a hash map using separate chaining for collision resolution.
# It contains methods to modify the hash map and retrieve information about the hash map.

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
        Puts the given key-value pair into this hash table.
        :param key: The key for the value.
        :param value: The value associated with the key.
        """
        # Double the capacity of the table if the table load is >= 1
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)
        hash = self._get_hash(key)
        # If the key was not present or removed, increment the size
        if not self._buckets[hash].remove(key):
            self._size += 1
        self._buckets[hash].insert(key, value)

    def empty_buckets(self) -> int:
        """
        Returns the amount of empty buckets in this hash table.
        :return: The amount of empty buckets in this hash table.
        """
        empty_buckets_count = 0
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                empty_buckets_count += 1
        return empty_buckets_count

    def table_load(self) -> float:
        """
        Returns the load factor for this hash table. (Size / Capacity)
        :return: The load factor for this hash table.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears this hash table without changing the capacity.
        """
        for i in range(self._capacity):
            self._buckets[i] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes this hash table with the new capacity where new capacity is > 1 and a prime number.
        :param new_capacity: The new capacity to resize this hash table to.
        """
        # If the new capacity is less than 1, do nothing
        if new_capacity < 1:
            return
        # If the new capacity is not prime, find the next prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)
        old_buckets = self._buckets
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0
        # Fill new buckets with empty linked lists
        for i in range(new_capacity):
            self._buckets.append(LinkedList())
        # Rehash all key-value pairs
        for i in range(old_buckets.length()):
            for node in old_buckets[i]:
                self.put(node.key, node.value)

    def get(self, key: str):
        """
        Returns a value for the given key, or None if the key is not present in the hash table.
        :param key: The key to find the matching value of.
        :return: A value for key, or None if the key is not present in the hash table.
        """
        hash = self._get_hash(key)
        node = self._buckets[hash].contains(key)
        return None if node is None else node.value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is present, otherwise False.
        :return: True if the given key is present, otherwise False.
        """
        return self.get(key) is not None

    def remove(self, key: str) -> None:
        """
        Removes the given key-value pairing from the hash table.
        :param key: The key to remove the key-value pairing of.
        """
        hash = self._get_hash(key)
        # If the key was present and removed, decrement the size
        if self._buckets[hash].remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a new dynamic array where each element is a tuple containing the key-value pairings in this hash table.
        :return: A dynamic array where each element is a tuple containing the key-value pairings in this hash table.
        """
        key_values = DynamicArray()
        for i in range(self._capacity):
            for node in self._buckets[i]:
                key_values.append((node.key, node.value))
        return key_values

    def _get_hash(self, key: str) -> int:
        """
        Helper method to return a hash index based on a given key.
        :param key: The key to return the hash of.
        :return: The hash index of the key.
        """
        return self._hash_function(key) % self._capacity


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Returns a tuple containing a dynamic array of the mode(s) of the given dynamic array and the number of times
    the mode(s) appear.
    :param da: The dynamic array to find the mode(s) of.
    :return: A tuple containing a dynamic array of the mode(s) of the given dynamic array and the number of times
        the mode(s) appear.
    """
    map = HashMap()
    # Map each value to the number of times it appears in the array
    for i in range(da.length()):
        value = da[i]
        map.put(value, map.get(value) + 1 if map.contains_key(value) else 1)
    mode = 0
    mode_arr = DynamicArray()
    keys_and_values = map.get_keys_and_values()
    # Find the mode and all values that appear the same number of times as the mode
    for i in range(keys_and_values.length()):
        key, value = keys_and_values[i]
        # If the value is greater than the current mode, set the mode to the value and clear the mode array
        if value > mode:
            mode = value
            mode_arr = DynamicArray()
            mode_arr.append(key)
        # If the value is equal to the current mode, add the value to the mode array
        elif value == mode:
            mode_arr.append(key)
    return mode_arr, mode


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
