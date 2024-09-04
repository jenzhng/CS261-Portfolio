# Name: Jenny Zhong
# OSU Email: zhongje@oregonstate.edu
# Course: CS261 - Data Structures, Section 401
# Assignment: Assignment 6 - Hash Implementation
# Due Date: 08/15/23
# Description: Hash Map Implementation - Open Addressing using Dynamic Array and HashEntry

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        """
        self._buckets = DynamicArray()
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
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
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the key exists, replace its value.
        """
        if self.table_load() >= 0.5:
            self.resize_table(2 * self._capacity)

        hash_index = self._hash_function(key) % self._capacity
        i = 0
        while True:
            quad_index = (hash_index + i ** 2) % self._capacity
            bucket_entry = self._buckets.get_at_index(quad_index)

            if bucket_entry is None or bucket_entry.is_tombstone:
                self._buckets.set_at_index(quad_index, HashEntry(key, value))
                self._size += 1
                return
            elif bucket_entry.key == key:
                if bucket_entry.is_tombstone:
                    self._size += 1
                self._buckets.set_at_index(quad_index, HashEntry(key, value))
                return

            i += 1

    def table_load(self) -> float:
        """
        Return the current hash table load factor
        """
        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets in the hash table
        """
        return sum(1 for i in range(self._capacity) if self._buckets.get_at_index(i) is None)

    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of the internal hash table and rehash all entries
        """
        if new_capacity <= self._size:
            return

        new_capacity = self._next_prime(new_capacity)
        new_table = HashMap(new_capacity, self._hash_function)

        for i in range(self._capacity):
            entry = self._buckets.get_at_index(i)
            if entry and not entry.is_tombstone:
                new_table.put(entry.key, entry.value)

        self._buckets = new_table._buckets
        self._capacity = new_table.get_capacity()
        self._size = new_table.get_size()

    def get(self, key: str) -> object:
        """
        Return the value associated with the given key
        """
        hash_index = self._hash_function(key) % self._capacity
        i = 0
        while True:
            quad_index = (hash_index + i ** 2) % self._capacity
            bucket_entry = self._buckets.get_at_index(quad_index)

            if bucket_entry is None:
                return None
            if bucket_entry.key == key and not bucket_entry.is_tombstone:
                return bucket_entry.value

            i += 1

    def contains_key(self, key: str) -> bool:
        """
        Return True if the given key is in the hash map
        """
        return self.get(key) is not None

    def remove(self, key: str) -> None:
        """
        Remove the given key and its associated value from the hash map
        """
        hash_index = self._hash_function(key) % self._capacity
        i = 0
        while True:
            quad_index = (hash_index + i ** 2) % self._capacity
            bucket_entry = self._buckets.get_at_index(quad_index)

            if bucket_entry is None:
                return
            if bucket_entry.key == key and not bucket_entry.is_tombstone:
                bucket_entry.is_tombstone = True
                self._size -= 1
                return

            i += 1

    def clear(self) -> None:
        """
        Clear the contents of the hash map
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a dynamic array of key/value pairs in the hash map
        """
        da = DynamicArray()
        for i in range(self._capacity):
            entry = self._buckets.get_at_index(i)
            if entry and not entry.is_tombstone:
                da.append((entry.key, entry.value))
        return da

    def __iter__(self):
        """
        Enable the hash map to be iterable
        """
        self._iter_index = 0
        return self

    def __next__(self):
        """
        Return the next item in the hash map
        """
        while self._iter_index < self._capacity:
            entry = self._buckets.get_at_index(self._iter_index)
            self._iter_index += 1
            if entry and not entry.is_tombstone:
                return entry
        raise StopIteration

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

  # print("\nPDF - put example 1")
  # print("-------------------")
  # m = HashMap(53, hash_function_1)
  # for i in range(150):
  #   m.put('str' + str(i), i * 100)
  #   if i % 25 == 24:
  #     print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(),
  #           m.get_capacity())

  # print("\nPDF - put example 2")
  # print("-------------------")
  # m = HashMap(41, hash_function_2)
  # for i in range(50):
  #   m.put('str' + str(i // 3), i * 100)
  #   if i % 10 == 9:
  #     print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(),
  #           m.get_capacity())

  # print("\nPDF - table_load example 1")
  # print("--------------------------")
  # m = HashMap(101, hash_function_1)
  # print(round(m.table_load(), 2))
  # m.put('key1', 10)
  # print(round(m.table_load(), 2))
  # m.put('key2', 20)
  # print(round(m.table_load(), 2))
  # m.put('key1', 30)
  # print(round(m.table_load(), 2))

  # print("\nPDF - table_load example 2")
  # print("--------------------------")
  # m = HashMap(53, hash_function_1)
  # for i in range(50):
  #   m.put('key' + str(i), i * 100)
  #   if i % 10 == 0:
  #     print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

  # print("\nPDF - empty_buckets example 1")
  # print("-----------------------------")
  # m = HashMap(101, hash_function_1)
  # print(m.empty_buckets(), m.get_size(), m.get_capacity())
  # m.put('key1', 10)
  # print(m.empty_buckets(), m.get_size(), m.get_capacity())
  # m.put('key2', 20)
  # print(m.empty_buckets(), m.get_size(), m.get_capacity())
  # m.put('key1', 30)
  # print(m.empty_buckets(), m.get_size(), m.get_capacity())
  # m.put('key4', 40)
  # print(m.empty_buckets(), m.get_size(), m.get_capacity())

  # print("\nPDF - empty_buckets example 2")
  # print("-----------------------------")
  # m = HashMap(53, hash_function_1)
  # for i in range(150):
  #   m.put('key' + str(i), i * 100)
  #   if i % 30 == 0:
  #     print(m.empty_buckets(), m.get_size(), m.get_capacity())

  # print("\nPDF - resize example 1")
  # print("----------------------")
  # m = HashMap(20, hash_function_1)
  # m.put('key1', 10)
  # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
  # m.resize_table(30)
  # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

  # print("\nPDF - resize example 2")
  # print("----------------------")
  # m = HashMap(75, hash_function_2)
  # keys = [i for i in range(25, 1000, 13)]
  # for key in keys:
  #   m.put(str(key), key * 42)
  # print(m.get_size(), m.get_capacity())

  # for capacity in range(111, 1000, 117):
  #   m.resize_table(capacity)

  #   if m.table_load() > 0.5:
  #     print(
  #         f"Check that the load factor is acceptable after the call to resize_table().\n"
  #         f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5"
  #     )

  #   m.put('some key', 'some value')
  #   result = m.contains_key('some key')
  #   m.remove('some key')

  #   for key in keys:
  #     # all inserted keys must be present
  #     result &= m.contains_key(str(key))
  #     # NOT inserted keys must be absent
  #     result &= not m.contains_key(str(key + 1))
  #   print(capacity, result, m.get_size(), m.get_capacity(),
  #         round(m.table_load(), 2))

  # print("\nPDF - get example 1")
  # print("-------------------")
  # m = HashMap(31, hash_function_1)
  # print(m.get('key'))
  # m.put('key1', 10)
  # print(m.get('key1'))

  # print("\nPDF - get example 2")
  # print("-------------------")
  # m = HashMap(151, hash_function_2)
  # for i in range(200, 300, 7):
  #   m.put(str(i), i * 10)
  # print(m.get_size(), m.get_capacity())
  # for i in range(200, 300, 21):
  #   print(i, m.get(str(i)), m.get(str(i)) == i * 10)
  #   print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

  # print("\nPDF - contains_key example 1")
  # print("----------------------------")
  # m = HashMap(11, hash_function_1)
  # print(m.contains_key('key1'))
  # m.put('key1', 10)
  # m.put('key2', 20)
  # m.put('key3', 30)
  # print(m.contains_key('key1'))
  # print(m.contains_key('key4'))
  # print(m.contains_key('key2'))
  # print(m.contains_key('key3'))
  # m.remove('key3')
  # print(m.contains_key('key3'))

  # print("\nPDF - contains_key example 2")
  # print("----------------------------")
  # m = HashMap(79, hash_function_2)
  # keys = [i for i in range(1, 1000, 20)]
  # for key in keys:
  #   m.put(str(key), key * 42)
  # print(m.get_size(), m.get_capacity())
  # result = True
  # for key in keys:
  #   # all inserted keys must be present
  #   result &= m.contains_key(str(key))
  #   # NOT inserted keys must be absent
  #   result &= not m.contains_key(str(key + 1))
  # print(result)

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
