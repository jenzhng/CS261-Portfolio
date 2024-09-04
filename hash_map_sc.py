# Name: Jenny Zhong
# OSU Email: zhongje@oregonstate.edu
# Course: CS261 - Data Structures, Section 401
# Assignment: Assignment 6 - Hash Implementation
# Due Date: 08/15/23
# Description: Hash Map Implementation - Chaining using Dynamic Array and Linked List


from a6_include import (DynamicArray, LinkedList, hash_function_1,
                        hash_function_2)


class HashMap:

    def __init__(self, capacity: int = 11, function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
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
        Increment from given number and find the closest prime number
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

    def put(self, key: str, value: object) -> None:
        """
        Update or add key/value pair in the hash map
        """
        if self.table_load() >= 1.0:
            self.resize_table(2 * self._capacity)

        h_index = self._hash_function(key) % self.get_capacity()
        bucket = self._buckets.get_at_index(h_index)
        node = bucket.contains(key)

        if node:
            node.value = value
        else:
            bucket.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        count = 0
        for i in range(self.get_capacity()):
            if self._buckets.get_at_index(i).length() == 0:
                count += 1
        return count

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        return self.get_size() / self.get_capacity()

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying hash table capacity
        """
        for i in range(self.get_capacity()):
            self._buckets.set_at_index(i, LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table and rehashes all key/value pairs
        """
        if new_capacity < 1:
            return

        new_capacity = self._next_prime(new_capacity)
        new_table = HashMap(new_capacity, self._hash_function)

        for i in range(self.get_capacity()):
            bucket = self._buckets.get_at_index(i)
            for node in bucket:
                new_table.put(node.key, node.value)

        self._buckets = new_table._buckets
        self._capacity = new_table._capacity
        self._size = new_table._size

    def get(self, key: str):
        """
        Returns the value associated with the key, or None if the key is not present
        """
        h_index = self._hash_function(key) % self.get_capacity()
        bucket = self._buckets.get_at_index(h_index)
        node = bucket.contains(key)
        return node.value if node else None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the key is in the hash map, False otherwise
        """
        h_index = self._hash_function(key) % self.get_capacity()
        bucket = self._buckets.get_at_index(h_index)
        return bucket.contains(key) is not None

    def remove(self, key: str) -> None:
        """
        Removes the key from the hash map
        """
        h_index = self._hash_function(key) % self.get_capacity()
        bucket = self._buckets.get_at_index(h_index)
        if bucket.remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns all key/value pairs as a DynamicArray of tuples
        """
        result = DynamicArray()
        for i in range(self.get_capacity()):
            bucket = self._buckets.get_at_index(i)
            for node in bucket:
                result.append((node.key, node.value))
        return result


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
  """
    TODO: Write this implementation
    """
  # if you'd like to use a hash map,
  # use this instance of your Separate Chaining HashMap
  map = HashMap()
  for j in range(da.length()):
    if not map.contains_key(da.get_at_index(j)):
      map.put(da.get_at_index(j), 1)
    else:
      map.put(da.get_at_index(j), map.get(da.get_at_index(j)) + 1)

  freq = 0
  new_arr = map.get_keys_and_values()
  mode_arr = DynamicArray()
  for j in range(new_arr.length()):
    if freq < new_arr.get_at_index(j)[1]:
      freq = new_arr.get_at_index(j)[1]

  for j in range(new_arr.length()):
    if new_arr.get_at_index(j)[1] == freq:
      mode_arr.append(new_arr.get_at_index(j)[0])

  return mode_arr, freq


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

  # print("\nPDF - put example 1")
  # print("-------------------")
  # m = HashMap(53, hash_function_1)
  # for i in range(150):
  #     m.put('str' + str(i), i * 100)
  #     if i % 25 == 24:
  #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

  # print("\nPDF - put example 2")
  # print("-------------------")
  # m = HashMap(41, hash_function_2)
  # for i in range(50):
  #     m.put('str' + str(i // 3), i * 100)
  #     if i % 10 == 9:
  #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
  # print(m)

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
  #     m.put('key' + str(i), i * 100)
  #     if i % 30 == 0:
  #         print(m.empty_buckets(), m.get_size(), m.get_capacity())

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
  #     m.put('key' + str(i), i * 100)
  #     if i % 10 == 0:
  #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

  # print("\nPDF - clear example 1")
  # print("---------------------")
  # m = HashMap(101, hash_function_1)
  # print(m.get_size(), m.get_capacity())
  # m.put('key1', 10)
  # m.put('key2', 20)
  # m.put('key1', 30)
  # print(m.get_size(), m.get_capacity())
  # m.clear()
  # print(m.get_size(), m.get_capacity())

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
  m = HashMap(20, hash_function_1)
  m.put('key1', 10)
  print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
  m.resize_table(30)
  print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

  print("\nPDF - resize example 3")
  print("----------------------")
  m = HashMap(41, hash_function_2)
  for i in range(50):
    m.put('str' + str(i // 3), i * 100)
  m.resize_table(60)

  # print("\nPDF - resize example 2")
  # print("----------------------")
  # m = HashMap(75, hash_function_2)
  # keys = [i for i in range(1, 1000, 13)]
  # for key in keys:
  #     m.put(str(key), key * 42)
  # print(m.get_size(), m.get_capacity())

  # for capacity in range(111, 1000, 117):
  #     m.resize_table(capacity)

  #     m.put('some key', 'some value')
  #     result = m.contains_key('some key')
  #     m.remove('some key')

  #     for key in keys:
  #         # all inserted keys must be present
  #         result &= m.contains_key(str(key))
  #         # NOT inserted keys must be absent
  #         result &= not m.contains_key(str(key + 1))
  #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

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
  #     m.put(str(i), i * 10)
  # print(m.get_size(), m.get_capacity())
  # for i in range(200, 300, 21):
  #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
  #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

  # print("\nPDF - contains_key example 1")
  # print("----------------------------")
  # m = HashMap(53, hash_function_1)
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
  #     m.put(str(key), key * 42)
  # print(m.get_size(), m.get_capacity())
  # result = True
  # for key in keys:
  #     # all inserted keys must be present
  #     result &= m.contains_key(str(key))
  #     # NOT inserted keys must be absent
  #     result &= not m.contains_key(str(key + 1))
  # print(result)

  # print("\nPDF - remove example 1")
  # print("----------------------")
  # m = HashMap(53, hash_function_1)
  # print(m.get('key1'))
  # m.put('key1', 10)
  # print(m.get('key1'))
  # m.remove('key1')
  # print(m.get('key1'))
  # m.remove('key4')

  # print("\nPDF - get_keys_and_values example 1")
  # print("------------------------")
  # m = HashMap(11, hash_function_2)
  # for i in range(1, 6):
  #     m.put(str(i), str(i * 10))
  # print(m.get_keys_and_values())

  # m.put('20', '200')
  # m.remove('1')
  # m.resize_table(2)
  # print(m.get_keys_and_values())

  # print("\nPDF - find_mode example 1")
  # print("-----------------------------")
  # da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
  # mode, frequency = find_mode(da)
  # print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

  # print("\nPDF - find_mode example 2")
  # print("-----------------------------")
  # test_cases = (
  #     ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
  #     ["one", "two", "three", "four", "five"],
  #     ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
  # )

  # for case in test_cases:
  #     da = DynamicArray(case)
  #     mode, frequency = find_mode(da)
  #     print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
