"""
hash_table.py
Hash Table implementation with chaining for collision resolution
"""

MAXHASH = 2999


class Node:
    """Node class for linked list in hash table bucket"""
    
    def __init__(self, key: str, value: int):
        """
        Initialize a node with a key-value pair
        
        Args:
            key: String key for the hash table
            value: Integer value associated with the key
        """
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    """Hash Table implementation using separate chaining"""
    
    def __init__(self, maxhash: int = MAXHASH):
        """Initialize hash table with empty buckets"""
        self.maxhash = maxhash
        self.buckets = [None] * self.maxhash
        self.count = 0
    
    def hash(self, key: str) -> int:
        """
        Hash function using polynomial rolling hash
        
        Args:
            key: String to hash
            
        Returns:
            Hash value (index in buckets array)
        """
        hash_value = 0
        for char in key:
            hash_value = hash_value * 31 + ord(char)
        return hash_value % self.maxhash
    
    def insert(self, key: str, value: int) -> None:
        """
        Insert or update a key-value pair in the hash table.
        If key exists, increment its value.
        
        Args:
            key: String key to insert
            value: Integer value to insert
        """
        index = self.hash(key)
        node = self.buckets[index]
        
        while node is not None:
            if node.key == key:
                node.value += value
                return
            node = node.next
        
        new_node = Node(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.count += 1
    
    def remove(self, key: str) -> None:
        """
        Remove a key-value pair from the hash table
        
        Args:
            key: String key to remove
        """
        index = self.hash(key)
        node = self.buckets[index]
        prev = None
        
        while node is not None:
            if node.key == key:
                if prev is None:
                    self.buckets[index] = node.next
                else:
                    prev.next = node.next
                self.count -= 1
                return
            prev = node
            node = node.next
    
    def increase(self, key: str) -> None:
        """
        Increment the value associated with a key by 1
        
        Args:
            key: String key to increment
        """
        index = self.hash(key)
        node = self.buckets[index]
        
        while node is not None:
            if node.key == key:
                node.value += 1
                return
            node = node.next
    
    def find(self, key: str) -> int:
        """
        Find the value associated with a key
        
        Args:
            key: String key to search for
            
        Returns:
            Value if key exists, 0 otherwise
        """
        index = self.hash(key)
        node = self.buckets[index]
        
        while node is not None:
            if node.key == key:
                return node.value
            node = node.next
        
        return 0
    
    def list_all_keys(self) -> None:
        """Print all key-value pairs in the hash table"""
        for i in range(self.maxhash):
            node = self.buckets[i]
            while node is not None:
                print(f"{node.key} : {node.value}")
                node = node.next
    
    def output_to_file(self, filename: str) -> None:
        """
        Write all key-value pairs to a file
        
        Args:
            filename: Name of output file
        """
        try:
            with open(filename, 'w') as outfile:
                for i in range(self.maxhash):
                    node = self.buckets[i]
                    while node is not None:
                        outfile.write(f"{node.key} : {node.value}\n")
                        node = node.next
        except IOError as e:
            print(f"Error: could not open file {filename}: {e}")
    
    def get_count(self) -> int:
        """
        Get the number of unique keys in the hash table
        
        Returns:
            Count of unique keys
        """
        return self.count
    
    def get_bucket(self, index: int) -> Node:
        """
        Get the head node of a bucket
        
        Args:
            index: Bucket index
            
        Returns:
            Head node of the bucket or None
        """
        if index < 0 or index >= self.maxhash:
            return None
        return self.buckets[index]
    
    def get_bucket_sizes(self) -> list:
        """
        Get the size (number of collisions) for each bucket
        
        Returns:
            List of tuples (bucket_index, collision_count)
        """
        bucket_sizes = []
        for i in range(self.maxhash):
            collision_count = 0
            node = self.buckets[i]
            while node is not None:
                collision_count += 1
                node = node.next
            bucket_sizes.append((i, collision_count))
        return bucket_sizes