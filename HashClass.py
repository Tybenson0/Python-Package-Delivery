# Create Hash Map objects
class CreateHashMap:
    def __init__(self, capacity):
        self.list = []
        for i in range(capacity):
            self.list.append([])

    # Inserts new key, value pair into the hash table/map
    def insert(self, key, item):  # does both insert and update
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        # Update Key/Value if key exists
        for kv in bucket_list:  
            if kv[0] == key:
                kv[1] = item
                return True

        # If not in hash table, insert
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Lookup items in hash table ( 0 - 0 )
    def lookup(self, key):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
        for pair in bucket_list:
            if key == pair[0]:
                return pair[1]
        return None  

    # Removes item from hash table
    def hash_remove(self, key):
        slot = hash(key) % len(self.list)
        bucket_list = self.list[slot]

    # Find the key-value pair and remove it
        for pair in bucket_list:
            if pair[0] == key:
                bucket_list.remove(pair)
                return True  # Indicate successful removal

        return False  # Indicate key not found
