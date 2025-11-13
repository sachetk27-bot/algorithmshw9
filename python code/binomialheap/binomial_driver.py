"""
Interactive CLI for Binomial Heap operations
Supports: Make-heap, Insert, Minimum, ExtractMin, Union, Decrease-Key, Delete
"""
from binomial_heap import BinomialHeap, BinomialNode, INT_MAX
import sys


class InteractiveBinomialHeap:
    def __init__(self):
        self.heap = BinomialHeap()
        self.node_map = {}  # Maps node IDs to actual nodes for decrease/delete operations
        self.next_node_id = 0
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*60)
        print("BINOMIAL HEAP CLI")
        print("="*60)
        print("Options: 1) Make-Heap  2) Insert  3) Find-Min  4) Extract-Min")
        print("         5) Union  6) Decrease-Key  7) Delete  8) Display")
        print("         9) Show Nodes  0) Exit")
        print("="*60)
    
    def make_heap(self):
        """Make-Heap operation"""
        self.heap = BinomialHeap()
        self.node_map = {}
        self.next_node_id = 0
        print("✓ New empty heap created!")
    
    def insert(self):
        """Insert operation"""
        try:
            key = int(input("Enter the key to insert: "))
            node = self.heap.insert(key)
            node_id = self.next_node_id
            self.node_map[node_id] = node
            self.next_node_id += 1
            print(f"✓ Inserted key {key} (Node ID: {node_id})")
        except ValueError:
            print("✗ Invalid input. Please enter an integer.")
    
    def find_min(self):
        """Find-Min operation"""
        min_node = self.heap.find_min()
        if min_node is None:
            print("✗ Heap is empty!")
        else:
            print(f"✓ Minimum key in heap: {min_node.key}")
    
    def extract_min(self):
        """Extract-Min operation"""
        if self.heap.head is None:
            print("✗ Heap is empty!")
            return
        
        min_val = self.heap.extract_min()
        
        if min_val == INT_MAX:
            print("✗ Heap is empty!")
            return
        
        # Clean up node_map: remove the extracted node
        # We need to identify which node had this value and was extracted
        # Since extract_min removes the min node, we should clean up invalid references
        nodes_to_remove = []
        for nid, node in self.node_map.items():
            # Check if node is still in the heap by traversing from roots
            if not self._node_in_heap(node):
                nodes_to_remove.append(nid)
        
        for nid in nodes_to_remove:
            del self.node_map[nid]
        
        print(f"✓ Extracted minimum: {min_val}")
    
    def _node_in_heap(self, target_node):
        """Check if a node is still in the heap"""
        if self.heap.head is None:
            return False
        
        # BFS through all nodes in the heap
        visited = set()
        stack = [self.heap.head]
        
        while stack:
            node = stack.pop()
            if node is None or id(node) in visited:
                continue
            
            visited.add(id(node))
            
            if node is target_node:
                return True
            
            if node.child:
                stack.append(node.child)
            if node.sibling:
                stack.append(node.sibling)
        
        return False
    
    def union(self):
        """Union operation"""
        print("\nCreating a second heap to union with...")
        try:
            num_elements = int(input("How many elements in the second heap? "))
            if num_elements < 0:
                print("✗ Number must be non-negative.")
                return
            
            other_heap = BinomialHeap()
            print(f"Enter {num_elements} keys for the second heap:")
            for i in range(num_elements):
                key = int(input(f"  Key {i+1}: "))
                other_heap.insert(key)
            
            print("\nFirst heap (before union):")
            self.heap.print_tree()
            print("\nSecond heap (before union):")
            other_heap.print_tree()
            
            self.heap.union_heaps(other_heap)
            print("\n✓ Heaps successfully unioned!")
            print("Result:")
            self.heap.print_tree()
        except ValueError:
            print("✗ Invalid input. Please enter integers.")
    
    def decrease_key(self):
        """Decrease-Key operation"""
        if not self.node_map:
            print("\n✗ No tracked nodes in heap!")
            return
            
        self.show_nodes()
        try:
            node_id = int(input("Enter the Node ID to decrease: "))
            if node_id not in self.node_map:
                print("✗ Invalid Node ID!")
                return
            
            node = self.node_map[node_id]
            
            # Verify node is still in heap
            if not self._node_in_heap(node):
                print(f"✗ Node ID {node_id} is no longer in the heap!")
                del self.node_map[node_id]
                return
            
            print(f"Current key value: {node.key}")
            new_key = int(input("Enter the new key value: "))
            
            if new_key > node.key:
                print(f"✗ New key ({new_key}) must be <= current key ({node.key})")
                return
            
            result = self.heap.decrease_key(node, new_key)
            if result is None:
                print("✗ Decrease key operation failed!")
            else:
                print(f"✓ Successfully decreased node {node_id} to {new_key}")
        except ValueError:
            print("✗ Invalid input. Please enter integers.")
    
    def delete(self):
        """Delete operation"""
        if not self.node_map:
            print("\n✗ No tracked nodes in heap!")
            return
            
        self.show_nodes()
        try:
            node_id = int(input("Enter the Node ID to delete: "))
            if node_id not in self.node_map:
                print("✗ Invalid Node ID!")
                return
            
            node = self.node_map[node_id]
            
            # Verify node is still in heap
            if not self._node_in_heap(node):
                print(f"✗ Node ID {node_id} is no longer in the heap!")
                del self.node_map[node_id]
                return
            
            original_key = node.key
            deleted_val = self.heap.delete_node(node)
            
            if deleted_val == INT_MAX:
                print("✗ Delete operation failed!")
            else:
                del self.node_map[node_id]
                print(f"✓ Successfully deleted node {node_id} (key was {original_key})")
        except ValueError:
            print("✗ Invalid input. Please enter an integer.")
    
    def display_heap(self):
        """Display heap structure"""
        if self.heap.head is None:
            print("\n✗ Heap is empty!")
        else:
            print("\nHeap structure:")
            self.heap.print_tree()
    
    def show_nodes(self):
        """Show all tracked nodes with their IDs"""
        if not self.node_map:
            print("\n✗ No tracked nodes in heap!")
            return
        
        # Clean up stale references
        valid_nodes = {}
        for node_id, node in self.node_map.items():
            if self._node_in_heap(node):
                valid_nodes[node_id] = node
        
        self.node_map = valid_nodes
        
        if not self.node_map:
            print("\n✗ No tracked nodes in heap!")
            return
        
        print("\nTracked nodes:")
        print("-" * 40)
        for node_id, node in sorted(self.node_map.items()):
            print(f"  Node ID {node_id}: key = {node.key}")
        print("-" * 40)
    
    def run(self):
        """Main interactive loop"""
        print("\nWelcome to Binomial Heap Interactive CLI!")
        self.make_heap()
        
        while True:
            self.display_menu()
            try:
                choice = input("Enter your choice (0-9): ").strip()
                
                if choice == '0':
                    print("\nThank you for using Binomial Heap CLI. Goodbye!")
                    sys.exit(0)
                elif choice == '1':
                    self.make_heap()
                elif choice == '2':
                    self.insert()
                elif choice == '3':
                    self.find_min()
                elif choice == '4':
                    self.extract_min()
                elif choice == '5':
                    self.union()
                elif choice == '6':
                    self.decrease_key()
                elif choice == '7':
                    self.delete()
                elif choice == '8':
                    self.display_heap()
                elif choice == '9':
                    self.show_nodes()
                else:
                    print("✗ Invalid choice. Please enter a number between 0 and 9.")
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"✗ An error occurred: {e}")


def main():
    cli = InteractiveBinomialHeap()
    cli.run()


if __name__ == '__main__':
    main()