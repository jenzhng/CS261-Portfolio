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
    while factor**2 <= capacity:
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
    Method updates the key/value pair in the hash map. If the given key already exists in
the hash map, its associated value must be replaced with the new value. If the given key is
not in the hash map, a new key/value pair must be added.
    Hash table is resized to double current capacity when table load is >= 0.5 
    Params: key: str, value: object
    Returns: None
    """
    # check if table load is greater than or equal to 0.5, if so resize table
    if self.table_load() >= 0.5:
      self.resize_table(2 * self._capacity)

    hash_index = self._hash_function(key) % self._capacity

    # if bucket is empty then insert the key value pair and increase size by 1
    if self._buckets.get_at_index(hash_index) == None:
      self._buckets.set_at_index(hash_index, HashEntry(key, value))
      self._size += 1

    else:
      i = 1
      quad_index = hash_index
      while self._buckets.get_at_index(quad_index):
        # if hash contains key, then replace with new value, do not increase size and return
        # if index was a tombstone then increase size
        if self._buckets.get_at_index(quad_index).key == key:
          if self._buckets.get_at_index(quad_index).is_tombstone == True:
            self._buckets.set_at_index(quad_index, HashEntry(key, value))
            self._size += 1
            self._buckets.get_at_index(quad_index).is_tombstone = False
          else:
            self._buckets.set_at_index(quad_index, HashEntry(key, value))
          return
        quad_index = (hash_index + i**2) % self._capacity
        i += 1

      self._buckets.set_at_index(quad_index, HashEntry(key, value))
      self._size += 1

  def table_load(self) -> float:
    """
    Method that returns the current hash table load factor.
    Params: None
    Returns: float
    """
    load = self.get_size() / self.get_capacity()
    return load

  def empty_buckets(self) -> int:
    """
    Method returns the number of empty buckets in the hash table
    Params: None
    Returns: int
    """
    count = self._capacity - self._size
    return count

  def resize_table(self, new_capacity: int) -> None:
    """
    Method that changes the capacity of the internal hash table. All existing key/value pairs
must remain in the new hash map, and all hash table links must be rehashed. 
    Check if new_capacity is not less than or equal the current number of elements; if so, the method does nothing.
    If new_capacity is greater than number of current elements, make sure it is a prime number. If not, rounds to nearest prime number.
    Params: new_capacity: int
    Returns: None
    """
    # check if new_capacity is greater than number of current elements, if not, return nothing
    if new_capacity <= self._size:
      return

    # if new_capacity is not a prime number, find next prime
    if self._is_prime(new_capacity) != True:
      new_capacity = self._next_prime(new_capacity)

    # initialize new table with same hash function
    table = HashMap(new_capacity, self._hash_function)

    if new_capacity == 2:
      table._capacity = 2

    for i in self:
      if i != None:
        table.put(i.key, i.value)

    # assign new values to self
    self._buckets = table._buckets
    self._capacity = table.get_capacity()
    self._size = table._size

  def get(self, key: str) -> object:
    """
    Method that returns the value associated with the given key. If the key is not in the hash map, the method returns None.
    Params: key: str
    Returns: object
    """
    for i in self:
      if i != None:
        if i.key == key and not i.is_tombstone:
          return i.value

    return None

  def contains_key(self, key: str) -> bool:
    """
    Method returns True if the given key is in the hash map, otherwise it returns False. An empty hash map does not contain any keys.
    Params: key:str
    Returns: bool
    """
    for i in self:
      if i != None:
        if i.key == key and not i.is_tombstone:
          return True
    return False

  def remove(self, key: str) -> None:
    """
    Method that removes the given key and its associated value from the hash map. If the key is not in the hash map, the method does nothing (no exception needs to be raised)
    Params: key: str
    Returns: None
    """
    for i in self:
      if i != None:
        if i.key == key and not i.is_tombstone:
          i.is_tombstone = True
          self._size -= 1

  def clear(self) -> None:
    """
    Method that clears the contents of the hash map without changing the underlying hash table capacity.
    Params: None
    Returns: None
    """
    self._buckets = DynamicArray()
    for i in range(self._capacity):
      self._buckets.append(None)
    self._size = 0

  def get_keys_and_values(self) -> DynamicArray:
    """
    Method that returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map. The order of the keys in the dynamic array does not matter.
    Params: None
    Returns: DynamicArray
    """
    new_da = DynamicArray()

    for i in self:
      if i and not i.is_tombstone:
        new_da.append((i.key, i.value))

    return new_da

  def __iter__(self):
    """
    Method that enables the hash map to iterate across itself.
    Params: None
    Returns None
    """
    self.index = 0
    return self

  def __next__(self):
    """
    Method that will return the next item in the hash map, based on the current location of the iterator. 
    Params: None
    Returns None
    """
    try:
      val = None
      while val == None or val.is_tombstone == True:
        val = self._buckets.get_at_index(self.index)
        self.index += 1
    except DynamicArrayException:
      raise StopIteration

    return val


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
