"""
hash.py
Interactive program to analyze word frequencies with different MAXHASH values
"""

import math
import sys
from pathlib import Path


def variance_calc(total_sum: int, n: int, bucket_sizes: list) -> float:
    """
    Calculate the variance of bucket sizes
    
    Args:
        total_sum: Sum of all bucket values
        n: Number of buckets
        bucket_sizes: List of (index, size) tuples
        
    Returns:
        Variance of bucket sizes
    """
    mean = total_sum / n
    sq_diff = 0
    
    for _, size in bucket_sizes:
        sq_diff += (size - mean) ** 2
    
    return sq_diff / n


class Node:
    def __init__(self, key: str, value: int):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self, maxhash: int = 30):
        self.maxhash = maxhash
        self.buckets = [None] * self.maxhash
        self.count = 0
    
    def hash(self, key: str) -> int:
        hash_value = 0
        for char in key:
            hash_value = hash_value * 31 + ord(char)
        return hash_value % self.maxhash
    
    def insert(self, key: str, value: int) -> None:
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
        index = self.hash(key)
        node = self.buckets[index]
        
        while node is not None:
            if node.key == key:
                node.value += 1
                return
            node = node.next
    
    def find(self, key: str) -> int:
        index = self.hash(key)
        node = self.buckets[index]
        
        while node is not None:
            if node.key == key:
                return node.value
            node = node.next
        
        return 0
    
    def output_to_file(self, filename: str) -> None:
        try:
            with open(filename, 'w') as outfile:
                for i in range(self.maxhash):
                    node = self.buckets[i]
                    while node is not None:
                        outfile.write(f"{node.key} : {node.value}\n")
                        node = node.next
        except IOError as e:
            print(f"Error: could not open file {filename}: {e}")
    
    def get_bucket_sizes(self) -> list:
        bucket_sizes = []
        for i in range(self.maxhash):
            collision_count = 0
            node = self.buckets[i]
            while node is not None:
                collision_count += 1
                node = node.next
            bucket_sizes.append((i, collision_count))
        return bucket_sizes


def analyze_hash_table(hash_table: HashTable, maxhash_value: int) -> None:
    """
    Analyze and display statistics for a hash table
    
    Args:
        hash_table: HashTable object to analyze
        maxhash_value: The MAXHASH value used
    """
    print("\n" + "="*60)
    print(f"ANALYSIS FOR MAXHASH = {maxhash_value}")
    print("="*60)
    
    print(f"\nOperations Test:")
    print(f"  Count of 'Alice': {hash_table.find('Alice')}")
    original_alice_count = hash_table.find('Alice')
    hash_table.increase("Alice")
    print(f"  Count of 'Alice' after increase: {hash_table.find('Alice')}")
    if original_alice_count > 0:
        hash_table.insert("Alice", -1)
    
    print("\n\nBucket Statistics (Hash no : No of collisions):")
    print("-" * 50)
    bucket_sizes = hash_table.get_bucket_sizes()
    total_sum = 0
    non_empty_buckets = 0
    
    for hash_no, size in bucket_sizes:
        if size > 0:
            print(f"  {hash_no} : {size}")
            total_sum += size
            non_empty_buckets += 1
    
    num_buckets = len(bucket_sizes)
    mean = total_sum / num_buckets
    variance = variance_calc(total_sum, num_buckets, bucket_sizes)
    std_dev = math.sqrt(variance)
    
    print("\n\nStatistical Analysis:")
    print(f"  Total Buckets: {num_buckets}")
    print(f"  Non-empty Buckets: {non_empty_buckets}")
    print(f"  Total Words: {total_sum}")
    print(f"  Mean Collisions per Bucket: {mean:.4f}")
    print(f"  Variance: {variance:.4f}")
    print(f"  Standard Deviation: {std_dev:.4f}")
    
    bucket_sizes_sorted = sorted(bucket_sizes, key=lambda x: x[1], reverse=True)
    
    top_10_percent = max(1, num_buckets // 10)
    print(f"\n\nTop 10% Buckets by Collision Count:")
    print("-" * 50)
    print("  Hash no : No of collisions")
    for i in range(top_10_percent):
        hash_no, size = bucket_sizes_sorted[i]
        print(f"  {hash_no} : {size}")


def load_words_from_file(hash_table: HashTable, filename: Path) -> bool:
    """
    Load words from file into hash table
    
    Args:
        hash_table: HashTable to populate
        filename: Path to text file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filename, 'r') as in_file:
            for line in in_file:
                words = line.split()
                for word in words:
                    hash_table.insert(word, 1)
        return True
    except FileNotFoundError:
        print(f"✗ Error: File '{filename}' not found")
        return False


def display_menu():
    """Display the main menu"""
    print("\n" + "="*60)
    print("     HASH TABLE INTERACTIVE CLI")
    print("="*60)
    print("1. Test with current MAXHASH")
    print("2. Enter a new MAXHASH value")
    print("3. Output word counts to file")
    print("0. Exit")
    print("="*60)


def main():
    """Main interactive function"""
    print("\nWelcome to Hash Table Interactive CLI!")
    print(f"Default MAXHASH: 30")
    
    script_dir = Path(__file__).parent.absolute()
    filename = script_dir / "Alice.txt"
    
    if not filename.exists():
        print(f"✗ Error: File '{filename}' not found")
        sys.exit(1)
    
    current_maxhash = 30
    
    while True:
        display_menu()
        choice = input("Enter your choice (0-3): ").strip()
        
        if choice == '0':
            print("\nThank you for using Hash Table CLI. Goodbye!")
            sys.exit(0)
        
        elif choice == '1':
            print(f"\n⏳ Loading words from {filename.name} with MAXHASH={current_maxhash}...")
            hash_table = HashTable(current_maxhash)
            
            if load_words_from_file(hash_table, filename):
                print(f"✓ Successfully loaded words from {filename.name}")
                analyze_hash_table(hash_table, current_maxhash)
        
        elif choice == '2':
            try:
                new_maxhash = int(input("\nEnter new MAXHASH value (must be positive integer): ").strip())
                if new_maxhash <= 0:
                    print("✗ MAXHASH must be a positive integer!")
                    continue
                
                print(f"\n⏳ Loading words from {filename.name} with MAXHASH={new_maxhash}...")
                
                hash_table = HashTable(new_maxhash)
                
                if load_words_from_file(hash_table, filename):
                    print(f"✓ Successfully loaded words from {filename.name}")
                    current_maxhash = new_maxhash
                    analyze_hash_table(hash_table, current_maxhash)
                
            except ValueError:
                print("✗ Invalid input. Please enter a positive integer.")
        
        elif choice == '3':
            print(f"\n⏳ Loading words from {filename.name}...")
            hash_table = HashTable(current_maxhash)
            
            if load_words_from_file(hash_table, filename):
                output_file = script_dir / "word_counts.txt"
                try:
                    hash_table.output_to_file(str(output_file))
                    print(f"✓ Successfully wrote word counts to {output_file.name}")
                except IOError as e:
                    print(f"✗ Error writing to file: {e}")
        
        else:
            print("✗ Invalid choice. Please enter a number between 0 and 3.")


if __name__ == "__main__":
    main()